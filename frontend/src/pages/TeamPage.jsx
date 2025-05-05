import React, { useEffect, useState } from "react";
import { getTeams, createTeam } from "../utils/api";
import { useNavigate } from "react-router-dom";

export default function TeamPage() {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    name: "",
    team_size: 1,
    tech_skills: "",
    experience_level: "",
    deadline: ""
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  // Fetch teams on mount or after creation
  const fetchTeams = () => {
    getTeams()
      .then(ts => {
        setTeams(ts);
        if (ts.length > 0 && !selectedTeam) setSelectedTeam(ts[0]);
      })
      .catch(err => setError(err.detail || "Failed to fetch teams"));
  };

  useEffect(() => {
    fetchTeams();
    // eslint-disable-next-line
  }, []);

  const handleSelectTeam = (team) => {
    setSelectedTeam(team);
    setShowForm(false);
    setError("");
    setSuccess("");
  };

  const handleFormChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await createTeam({
        name: form.name,
        team_size: Number(form.team_size),
        tech_skills: form.tech_skills.split(",").map(s => s.trim()),
        experience_level: form.experience_level,
        deadline: form.deadline
        ? new Date(form.deadline).toISOString() 
        : undefined
      });
      setSuccess("Team created!");
      setShowForm(false);
      setForm({
        name: "",
        team_size: 1,
        tech_skills: "",
        experience_level: "",
        deadline: ""
      });
      fetchTeams();
    } catch (err) {
      setError(err.detail || "Create team failed");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <div className="flex justify-between items-center px-8 py-4 bg-white shadow">
        <h1 className="text-2xl font-bold text-blue-700">Teams</h1>
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          onClick={()=> navigate("/")}
        >
          Back to Home
        </button>
      </div>

      <div className="max-w-4xl mx-auto mt-10 bg-white p-8 rounded-lg shadow flex flex-col md:flex-row gap-8">
        {/* Team List */}
        <div className="w-full md:w-1/3">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold">Your Teams</h2>
            <button
              className="text-blue-600 hover:underline"
              onClick={() => { setShowForm(!showForm); setError(""); setSuccess(""); }}
            >
              {showForm ? "Cancel" : "Create New"}
            </button>
          </div>
          <ul>
            {teams.map(team => (
              <li
                key={team.id}
                className={`p-2 rounded cursor-pointer mb-2 ${selectedTeam && team.id === selectedTeam.id ? "bg-blue-100 font-bold" : "hover:bg-gray-100"}`}
                onClick={() => handleSelectTeam(team)}
              >
                {team.name}
              </li>
            ))}
          </ul>
        </div>

        {/* Team Details or Create Form */}
        <div className="w-full md:w-2/3">
          {showForm ? (
            <form className="space-y-4" onSubmit={handleCreateTeam}>
              <h2 className="text-lg font-semibold mb-2">Create New Team</h2>
              <input
                className="w-full px-3 py-2 border border-gray-300 rounded"
                name="name"
                value={form.name}
                onChange={handleFormChange}
                placeholder="Team Name"
                required
              />
              <input
                className="w-full px-3 py-2 border border-gray-300 rounded"
                name="team_size"
                type="number"
                min="1"
                value={form.team_size}
                onChange={handleFormChange}
                placeholder="Team Size"
                required
              />
              <input
                className="w-full px-3 py-2 border border-gray-300 rounded"
                name="tech_skills"
                value={form.tech_skills}
                onChange={handleFormChange}
                placeholder="Tech Skills (comma separated)"
                required
              />
              <input
                className="w-full px-3 py-2 border border-gray-300 rounded"
                name="experience_level"
                value={form.experience_level}
                onChange={handleFormChange}
                placeholder="Experience Level"
                required
              />
              <input
                className="w-full px-3 py-2 border border-gray-300 rounded"
                name="deadline"
                type="date"
                value={form.deadline}
                onChange={handleFormChange}
                placeholder="Deadline"
              />
              <button
                type="submit"
                className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                Create Team
              </button>
              {error && <div className="text-red-600">{error}</div>}
              {success && <div className="text-green-600">{success}</div>}
            </form>
          ) : selectedTeam ? (
            <div>
              <h2 className="text-lg font-semibold mb-2">{selectedTeam.name}</h2>
              <div className="mb-2"><b>Team Size:</b> {selectedTeam.team_size}</div>
              <div className="mb-2"><b>Tech Skills:</b> {selectedTeam.tech_skills.join(", ")}</div>
              <div className="mb-2"><b>Experience Level:</b> {selectedTeam.experience_level}</div>
              {selectedTeam.deadline && (
                <div className="mb-2"><b>Deadline:</b> {selectedTeam.deadline.slice(0, 10)}</div>
              )}
              <div className="mb-2"><b>Created At:</b> {selectedTeam.created_at ? selectedTeam.created_at.slice(0, 10) : "N/A"}</div>
            </div>
          ) : (
            <div className="text-gray-500">Select a team to see details.</div>
          )}
        </div>
      </div>
    </div>
  );
}