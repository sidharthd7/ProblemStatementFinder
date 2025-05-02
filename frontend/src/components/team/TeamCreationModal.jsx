import { useState } from 'react';

export default function TeamCreationModal({ isOpen, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    teamName: '',
    techSkills: '',
    teamSize: '',
    experienceLevel: '',
    deadline: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      teamName: '',
      techSkills: '',
      teamSize: '',
      experienceLevel: '',
      deadline: ''
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium leading-6 text-gray-900 mb-4">
            Create New Team
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="text"
                placeholder="Team Name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                value={formData.teamName}
                onChange={(e) => setFormData({...formData, teamName: e.target.value})}
                required
              />
            </div>
            <div>
              <input
                type="text"
                placeholder="Tech Skills"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                value={formData.techSkills}
                onChange={(e) => setFormData({...formData, techSkills: e.target.value})}
                required
              />
            </div>
            <div>
              <input
                type="number"
                placeholder="Team Size"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                value={formData.teamSize}
                onChange={(e) => setFormData({...formData, teamSize: e.target.value})}
                required
              />
            </div>
            <div>
              <input
                type="text"
                placeholder="Experience Level"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                value={formData.experienceLevel}
                onChange={(e) => setFormData({...formData, experienceLevel: e.target.value})}
                required
              />
            </div>
            <div>
              <input
                type="date"
                placeholder="Deadline"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                value={formData.deadline}
                onChange={(e) => setFormData({...formData, deadline: e.target.value})}
                required
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Create Team
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}