import { useState, useEffect } from 'react';

export default function TeamSelect({ selectedTeam, onSelect }) {
  const [teams, setTeams] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // TODO: Fetch teams from backend
    // Mock data for now
    setTeams([
      { id: 1, name: 'Team A' },
      { id: 2, name: 'Team B' },
      { id: 3, name: 'Team C' },
    ]);
  }, []);

  return (
    <div className="relative">
      <button
        type="button"
        className="inline-flex justify-between items-center w-48 rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selectedTeam ? selectedTeam.name : 'Select Team'}
        <svg
          className="-mr-1 ml-2 h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute z-10 mt-1 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
          <div className="py-1" role="menu">
            {teams.map((team) => (
              <button
                key={team.id}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                onClick={() => {
                  onSelect(team);
                  setIsOpen(false);
                }}
              >
                {team.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}