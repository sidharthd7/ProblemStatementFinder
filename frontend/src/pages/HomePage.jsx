import React, { useEffect, useState } from "react";
import { getTeams, uploadProblems } from "../utils/api";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Fetch teams on mount
  useEffect(() => {
    getTeams()
      .then(setTeams)
      .catch(err => setError(err.detail || "Failed to fetch teams"));
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults([]);
    setError("");
  };

  const handleTeamChange = (e) => {
    const teamId = e.target.value;
    setSelectedTeam(teamId);
    setResults([]);
    setError("");
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    setError("");
    setResults([]);
    if (!file || !selectedTeam) {
      setError("Please select a team and a file.");
      return;
    }
    setLoading(true);
    try {
      const res = await uploadProblems(file, selectedTeam);
      setResults(res);
    } catch (err) {
      setError(err.detail || "Upload failed");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <div className="flex justify-between items-center px-8 py-4 bg-white shadow">
        <div>
          <h1 className="text-2xl font-semibold text-blue-700">Problem Statement Finder</h1>
          <div className="flex flex-row gap-1 text-sm text-[#4d4d4d]">
            <h3 className="font-medium pr-2">Made By</h3>
            <a href="https://github.com/sidharthd7">Sidharth Dhawan</a>
            <p>   |   </p>
            <a href="https://github.com/HarshKumat">Harsh Kumat</a>
          </div>
        </div>
        
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          onClick={() => navigate("/team")}
        >
          Teams
        </button>
      </div>

      {/* Main Content */}
      <div className="max-w-2xl mx-auto mt-10 bg-white p-8 rounded-lg shadow">
        <form className="space-y-6" onSubmit={handleUpload}>
          <div>
            <label className="block font-semibold mb-1">Select Team</label>
            <select
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={selectedTeam || ""}
              onChange={handleTeamChange}
              required
            >
              <option value="" disabled>Select a team</option>
              {teams.map(team => (
                <option key={team.id} value={team.id}>
                  {team.name} ({team.team_size} members)
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block font-semibold mb-1">Upload Problem Statement File (.xlsx, .xls, .csv)</label>
            <input
              type="file"
              accept=".xlsx,.xls,.csv"
              className="w-full"
              onChange={handleFileChange}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
            disabled={loading}
          >
            {loading ? "Processing..." : "Upload & Get Top Results"}
          </button>
        </form>

        {error && <div className="mt-4 text-red-600 text-center">{error}</div>}

        {/* Results */}
        {results.length > 0 && (
          <div className="mt-8">
            <h2 className="text-lg font-bold mb-4 text-blue-700">Top 10 Results</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full border">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="px-4 py-2 border">Rank</th>
                    <th className="px-4 py-2 border">Problem Statement</th>
                    <th className="px-4 py-2 border">Match Score</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((item, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-2 border text-center">{idx + 1}</td>
                      <td className="px-4 py-2 border">{item.problem.title || item.problem.description}</td>
                      <td className="px-4 py-2 border text-center">{item.score}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}