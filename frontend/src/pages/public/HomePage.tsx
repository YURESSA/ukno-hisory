import { PublicLayout } from '@/layouts/PublicLayout/PublicLayout';

export const HomePage = () => {

  return (
    <PublicLayout>
      <div className="container" style={{ textAlign: 'center' }}>
        <h1 className="title-h1" style={{ marginBottom: '24px' }}>
          История УКНО
        </h1>
      </div>
    </PublicLayout>
  );
};
