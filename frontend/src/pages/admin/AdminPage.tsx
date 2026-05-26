import { useState } from 'react';
import { LoginForm } from '@/modules/auth/components/admin/LoginForm';
import { CreateProjectForm } from '@/modules/projects/components/admin/CreateProjectForm';
import { AdminProjectList } from '@/modules/projects/components/admin/AdminProjectList';
import { TimelineList } from '@/modules/timeline/components/admin/TimelineList';
import { CreateTimelineForm } from '@/modules/timeline/components/admin/CreateTimelineForm';
import { EnterpriseHistoryList } from '@/modules/enterprise_history/components/admin/EnterpriseHistoryList';
import { CreateEnterpriseHistoryForm } from '@/modules/enterprise_history/components/admin/CreateEnterpriseHistoryForm';
import { UserList } from '@/modules/users/components/admin/UserList';
import { CreateAdminForm } from '@/modules/users/components/admin/CreateAdminForm';
import { QuizQuestionList } from '@/modules/quiz/components/admin/QuizQuestionList';
import { CreateQuizQuestionForm } from '@/modules/quiz/components/admin/CreateQuizQuestionForm';
import { AdminLayout } from '@/layouts/AdminLayout/AdminLayout';

import '@/styles/admin.css';

export const AdminPage = () => {
  const [activeTab, setActiveTab] = useState<'projects' | 'timeline' | 'enterprise' | 'users' | 'quiz'>('projects');
  const token = localStorage.getItem('token');

  if (!token) {
    return <LoginForm />;
  }

  return (
    <AdminLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'projects' && (
        <div className="adm-module-row">
          <div className="adm-module-sidebar">
            <CreateProjectForm />
          </div>
          <div className="adm-module-main">
            <AdminProjectList />
          </div>
        </div>
      )}

      {activeTab === 'timeline' && (
        <div className="adm-module-row">
          <div className="adm-module-sidebar">
            <CreateTimelineForm />
          </div>
          <div className="adm-module-main">
            <TimelineList />
          </div>
        </div>
      )}

      {activeTab === 'enterprise' && (
        <div className="adm-module-row">
          <div className="adm-module-sidebar">
            <CreateEnterpriseHistoryForm />
          </div>
          <div className="adm-module-main">
            <EnterpriseHistoryList />
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="adm-module-row">
          <div className="adm-module-sidebar">
            <CreateAdminForm />
          </div>
          <div className="adm-module-main">
            <UserList />
          </div>
        </div>
      )}

      {activeTab === 'quiz' && (
        <div className="adm-module-row">
          <div className="adm-module-sidebar">
            <CreateQuizQuestionForm />
          </div>
          <div className="adm-module-main">
            <QuizQuestionList />
          </div>
        </div>
      )}
    </AdminLayout>
  );
};
