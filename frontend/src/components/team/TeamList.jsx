export default function TeamList({ teams, onTeamUpdate }) {
    const handleDeleteTeam = (teamId) => {
      // TODO: Connect with backend API
      onTeamUpdate(teams.filter(team => team.id !== teamId));
    };
  
    return (
      <div className="overflow-hidden rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Group ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Group Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Group Members
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {teams.map((team) => (
              <tr key={team.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {team.id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {team.teamName}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {team.teamSize}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleDeleteTeam(team.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete Team
                    </button>
                    <button
                      className="text-blue-600 hover:text-blue-900 ml-3"
                    >
                      Select Team
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
  
        {teams.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No teams created yet. Create a new team to get started.
          </div>
        )}
      </div>
    );
  }