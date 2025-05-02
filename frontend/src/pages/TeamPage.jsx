import { useState } from 'react';
import TeamList from '../components/team/TeamList';
import TeamCreationModal from '../components/team/TeamCreationModal';

export default function TeamPage() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [teams, setTeams] = useState([]);

  const handleCreateTeam = (newTeam) => {
    // TODO: Connect with backend API
    setTeams([...teams, { ...newTeam, id: Date.now() }]);
    setIsCreateModalOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow p-6">
            {/* Header */}
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-2xl font-bold text-gray-900">
                Team Management
              </h1>
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Create New Team
              </button>
            </div>

            {/* Team List */}
            <TeamList teams={teams} onTeamUpdate={setTeams} />

            {/* Create Team Modal */}
            <TeamCreationModal
              isOpen={isCreateModalOpen}
              onClose={() => setIsCreateModalOpen(false)}
              onSubmit={handleCreateTeam}
            />
          </div>
        </div>
      </div>
    </div>
  );
}