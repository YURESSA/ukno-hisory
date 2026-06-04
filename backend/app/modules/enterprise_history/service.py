from fastapi import HTTPException, status

from app.modules.enterprise_history.files import EnterpriseHistoryFileStorage
from app.modules.enterprise_history.models import (
    EnterpriseHistory,
    EnterpriseHistoryGalleryImage,
    EnterpriseHistorySlide,
)
from app.modules.enterprise_history.schemas import (
    EnterpriseHistoryAdminDetailRead,
    EnterpriseHistoryDetailRead,
    EnterpriseHistoryUpdate,
)
from app.modules.subdistricts.constants import normalize_subdistrict_name


class EnterpriseHistoryService:
    def __init__(self, repo, file_storage: EnterpriseHistoryFileStorage):
        self.repo = repo
        self.file_storage = file_storage

    async def create_item(
        self,
        *,
        title: str | None,
        subdistrict: str | None,
        general_subtitle: str | None,
        detail_subtitle: str | None,
        short_description: str | None,
        is_draft: bool,
        general_main_image,
        detail_main_image,
    ):
        general_main_image_path = None
        detail_main_image_path = None
        if general_main_image is not None:
            general_main_image_path = await self.file_storage.save_general_main_image(
                general_main_image
            )
        if detail_main_image is not None:
            detail_main_image_path = await self.file_storage.save_detail_main_image(
                detail_main_image
            )

        item = EnterpriseHistory(
            title=self._clean_text(title),
            subdistrict=self._normalize_subdistrict(subdistrict),
            general_subtitle=self._clean_text(general_subtitle),
            detail_subtitle=self._clean_text(detail_subtitle),
            short_description=self._clean_text(short_description),
            general_main_image=general_main_image_path,
            detail_main_image=detail_main_image_path,
            is_draft=is_draft,
        )
        self._validate_publishable(item, is_draft)
        item = await self.repo.create(item)
        return self._build_admin_detail(item)

    async def get_public_items(self, subdistrict: str | None = None):
        return await self.repo.get_public_all(
            subdistrict=(
                self._normalize_subdistrict(subdistrict)
                if subdistrict is not None
                else None
            )
        )

    async def get_admin_items(self, subdistrict: str | None = None):
        return await self.repo.get_all(
            subdistrict=(
                self._normalize_subdistrict(subdistrict)
                if subdistrict is not None
                else None
            )
        )

    async def get_public_item(self, item_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=False)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )
        return self._build_public_detail(item)

    async def get_admin_item(self, item_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )
        return self._build_admin_detail(item)

    async def update_item(self, item_id: int, *, data: EnterpriseHistoryUpdate):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        for field in (
            "title",
            "subdistrict",
            "general_subtitle",
            "detail_subtitle",
            "short_description",
        ):
            if field in data.model_fields_set:
                value = getattr(data, field)
                if field == "subdistrict":
                    setattr(item, field, self._normalize_subdistrict(value))
                else:
                    setattr(item, field, self._clean_text(value))

        if "is_draft" in data.model_fields_set:
            item.is_draft = data.is_draft

        self._validate_publishable(item, item.is_draft)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def update_general_main_image(self, item_id: int, image):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        old_image = item.general_main_image
        item.general_main_image = await self.file_storage.save_general_main_image(image)
        self._validate_publishable(item, item.is_draft)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if old_image is not None:
            self.file_storage.delete_image(old_image)
        return self._build_admin_detail(item)

    async def delete_general_main_image(self, item_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        image_path = item.general_main_image
        item.general_main_image = None
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if image_path is not None:
            self.file_storage.delete_image(image_path)
        return self._build_admin_detail(item)

    async def update_detail_main_image(self, item_id: int, image):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        old_image = item.detail_main_image
        item.detail_main_image = await self.file_storage.save_detail_main_image(image)
        self._validate_publishable(item, item.is_draft)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if old_image is not None:
            self.file_storage.delete_image(old_image)
        return self._build_admin_detail(item)

    async def delete_detail_main_image(self, item_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        image_path = item.detail_main_image
        item.detail_main_image = None
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if image_path is not None:
            self.file_storage.delete_image(image_path)
        return self._build_admin_detail(item)

    async def add_how_it_was_slide(
        self,
        item_id: int,
        *,
        text: str | None,
        image,
        order_index: int | None,
    ):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        cleaned_text = self._clean_text(text)
        image_path = None
        if image is not None:
            image_path = await self.file_storage.save_how_it_was_image(image)
        if cleaned_text is None and image_path is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Слайд должен содержать текст, изображение или оба поля",
            )

        target_index = self._normalize_insert_index(
            order_index,
            len(item.how_it_was_slides),
        )
        self._shift_slides_for_insert(item, target_index)
        slide = EnterpriseHistorySlide(
            enterprise_history_id=item.id,
            text=cleaned_text,
            image=image_path,
            order_index=target_index,
        )
        self.repo.session.add(slide)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def update_how_it_was_slide(
        self,
        item_id: int,
        slide_id: int,
        *,
        text_provided: bool,
        text: str | None,
        order_index: int | None,
    ):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        slide = self._find_slide(item, slide_id)

        if text_provided:
            slide.text = self._clean_text(text)
        if slide.text is None and slide.image is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Слайд должен содержать текст, изображение или оба поля",
            )

        if order_index is not None:
            self._move_slide(item, slide, order_index)

        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def update_how_it_was_slide_image(self, item_id: int, slide_id: int, image):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        slide = self._find_slide(item, slide_id)

        old_image = slide.image
        slide.image = await self.file_storage.save_how_it_was_image(image)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if old_image is not None:
            self.file_storage.delete_image(old_image)
        return self._build_admin_detail(item)

    async def delete_how_it_was_slide_image(self, item_id: int, slide_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        slide = self._find_slide(item, slide_id)
        if slide.text is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Нельзя удалить единственное содержимое слайда",
            )

        image_path = slide.image
        slide.image = None
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        if image_path is not None:
            self.file_storage.delete_image(image_path)
        return self._build_admin_detail(item)

    async def delete_how_it_was_slide(self, item_id: int, slide_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        slide = self._find_slide(item, slide_id)
        image_path = slide.image
        await self.repo.session.delete(slide)
        item.how_it_was_slides = [
            current for current in item.how_it_was_slides if current.id != slide_id
        ]
        self._reorder_slides(item)
        await self.repo.session.commit()
        if image_path is not None:
            self.file_storage.delete_image(image_path)
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def reorder_how_it_was_slides(self, item_id: int, slide_ids: list[int]):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        current_ids = [slide.id for slide in item.how_it_was_slides]
        if sorted(current_ids) != sorted(slide_ids):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Порядок слайдов должен содержать все текущие идентификаторы",
            )

        mapping = {slide.id: slide for slide in item.how_it_was_slides}
        ordered = [mapping[slide_id] for slide_id in slide_ids]
        for index, slide in enumerate(ordered):
            slide.order_index = index
        item.how_it_was_slides = ordered
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def add_gallery_images(self, item_id: int, images: list):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        start_position = len(item.gallery_images)
        for offset, image in enumerate(images):
            image_path = await self.file_storage.save_gallery_image(image)
            gallery_item = EnterpriseHistoryGalleryImage(
                enterprise_history_id=item.id,
                image=image_path,
                position=start_position + offset,
            )
            self.repo.session.add(gallery_item)

        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def delete_gallery_image(self, item_id: int, image_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        target = next((img for img in item.gallery_images if img.id == image_id), None)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Изображение галереи не найдено",
            )

        image_path = target.image
        await self.repo.session.delete(target)
        item.gallery_images = [img for img in item.gallery_images if img.id != image_id]
        self._reorder_gallery(item)
        await self.repo.session.commit()
        self.file_storage.delete_image(image_path)
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def reorder_gallery(self, item_id: int, image_ids: list[int]):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        current_ids = [image.id for image in item.gallery_images]
        if sorted(current_ids) != sorted(image_ids):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Порядок галереи должен содержать все текущие идентификаторы "
                    "изображений без пропусков и дубликатов"
                ),
            )

        mapping = {image.id: image for image in item.gallery_images}
        ordered = [mapping[image_id] for image_id in image_ids]
        for position, image in enumerate(ordered):
            image.position = position
        item.gallery_images = ordered
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id, include_drafts=True)
        return self._build_admin_detail(item)

    async def delete_item(self, item_id: int):
        item = await self.repo.get_by_id(item_id, include_drafts=True)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        image_paths = []
        if item.general_main_image:
            image_paths.append(item.general_main_image)
        if item.detail_main_image:
            image_paths.append(item.detail_main_image)
        image_paths.extend(
            slide.image for slide in item.how_it_was_slides if slide.image is not None
        )
        image_paths.extend(image.image for image in item.gallery_images)

        await self.repo.delete(item)
        for image_path in image_paths:
            self.file_storage.delete_image(image_path)

    def _validate_publishable(self, item: EnterpriseHistory, is_draft: bool):
        if is_draft:
            return

        required_fields = {
            "title": item.title,
            "subdistrict": item.subdistrict,
            "general_subtitle": item.general_subtitle,
            "detail_subtitle": item.detail_subtitle,
            "short_description": item.short_description,
            "general_main_image": item.general_main_image,
            "detail_main_image": item.detail_main_image,
        }
        missing_fields = [key for key, value in required_fields.items() if not value]
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Черновик нельзя опубликовать без обязательных полей: "
                    + ", ".join(missing_fields)
                ),
            )

    def _build_public_detail(
        self, item: EnterpriseHistory
    ) -> EnterpriseHistoryDetailRead:
        return EnterpriseHistoryDetailRead(
            id=item.id,
            title=item.title or "",
            subdistrict=item.subdistrict or "",
            subtitle=item.detail_subtitle or "",
            short_description=item.short_description or "",
            main_image=item.detail_main_image or "",
            how_it_was=item.how_it_was_slides,
            gallery=item.gallery_images,
        )

    def _build_admin_detail(
        self,
        item: EnterpriseHistory,
    ) -> EnterpriseHistoryAdminDetailRead:
        return EnterpriseHistoryAdminDetailRead(
            id=item.id,
            title=item.title,
            subdistrict=item.subdistrict,
            general_subtitle=item.general_subtitle,
            detail_subtitle=item.detail_subtitle,
            short_description=item.short_description,
            general_main_image=item.general_main_image,
            detail_main_image=item.detail_main_image,
            is_draft=item.is_draft,
            how_it_was=item.how_it_was_slides,
            gallery=item.gallery_images,
        )

    def _clean_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _normalize_subdistrict(self, value: str | None) -> str | None:
        cleaned = self._clean_text(value)
        if cleaned is None:
            return None
        try:
            return normalize_subdistrict_name(cleaned)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Неизвестный подрайон",
            ) from exc

    def _find_slide(
        self,
        item: EnterpriseHistory | None,
        slide_id: int,
    ) -> EnterpriseHistorySlide:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="История предприятия не найдена",
            )

        slide = next(
            (current for current in item.how_it_was_slides if current.id == slide_id),
            None,
        )
        if not slide:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Слайд не найден",
            )
        return slide

    def _normalize_insert_index(self, order_index: int | None, length: int) -> int:
        if order_index is None:
            return length
        return min(max(order_index, 0), length)

    def _shift_slides_for_insert(
        self, item: EnterpriseHistory, start_index: int
    ) -> None:
        for slide in item.how_it_was_slides:
            if slide.order_index >= start_index:
                slide.order_index += 1

    def _move_slide(
        self,
        item: EnterpriseHistory,
        slide: EnterpriseHistorySlide,
        new_index: int,
    ) -> None:
        ordered = sorted(
            item.how_it_was_slides, key=lambda current: current.order_index
        )
        ordered = [current for current in ordered if current.id != slide.id]
        target_index = min(max(new_index, 0), len(ordered))
        ordered.insert(target_index, slide)
        for index, current in enumerate(ordered):
            current.order_index = index
        item.how_it_was_slides = ordered

    def _reorder_slides(self, item: EnterpriseHistory) -> None:
        ordered = sorted(
            item.how_it_was_slides, key=lambda current: current.order_index
        )
        for index, slide in enumerate(ordered):
            slide.order_index = index
        item.how_it_was_slides = ordered

    def _reorder_gallery(self, item: EnterpriseHistory) -> None:
        for position, image in enumerate(item.gallery_images):
            image.position = position
