import React, { useEffect, useState, useRef } from "react";
import { getTeams, uploadProblems } from "../utils/api";
import { useNavigate } from "react-router-dom";
import ReactMarkdown from 'react-markdown'

export default function HomePage() {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [abortController, setAbortController] = useState(null);
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
    const controller = new AbortController();
    setAbortController(controller);
    try {
      const res = await uploadProblems(file, selectedTeam, controller.signal);
      console.log('API Response:', res)
      setResults(res.matches || []);
    } catch (err) {
      if(err.name === "AbortError"){
        setError("Upload cancelled.");
      } else{
        console.log('Upload Error:', err)
        setError(err.detail || err.message || "Upload failed");
      }
    }
    setLoading(false);
    setAbortController(null);
  };

  const handleCancel = () => {
    console.log("Cancelling...")
    if(abortController){
      abortController.abort();
    }
    setLoading(false);
    setAbortController(null);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <div className="flex sticky top-0 z-10 justify-between items-center px-8 py-4 bg-white shadow">
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
      <div className="max-w-4xl mx-auto mt-10 bg-white p-8 rounded-lg shadow">
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
          {!loading ? (
            <button
              type="submit"
              className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              disabled={loading}
            >
              Upload & Get Top Results
            </button>
          ) : (
            <button
              type="button"
              className="w-full py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
              onClick={handleCancel}
            >
              Cancel
            </button>
          )}
        </form>
            
        {loading && (
          <div className="mt-8 text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
            <p className="mt-2 text-gray-600">Processing your request...</p>
          </div>
        )}

        {error && <div className="mt-4 text-red-600 text-center">{error}</div>}

        {/* Results */}
        {results.length > 0 && (
          <div className="mt-8">
            <h2 className="text-lg font-bold mb-4 text-blue-700">Top Matches</h2>
            <div className="space-y-6">
              {results.map((match, idx) => (
                <div key={idx} className="border rounded-lg p-6 bg-white shadow-sm hover:shadow-md transition">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {match.problem_details?.description || 'No description available'}
                      </h3>
                      <p className="text-sm text-gray-500 mt-1">
                        Complexity: {match.problem_details?.complexity || 'N/A'} | 
                        Deadline: {match.problem_details?.deadline || 'N/A'} days
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round((match.similarity_score || 0 )* 100)}%
                      </div>
                      <div className="text-sm text-gray-500">Match Score</div>
                    </div>
                  </div>

                  {/* Required Skills */}
                  <div className="mb-4">
                    <h4 className="font-medium text-gray-700 mb-2">Required Skills:</h4>
                    <div className="flex flex-wrap gap-2">
                      {match.problem_details?.required_skills?.length > 0 ? (
                        match.problem_details.required_skills.map((skill, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                          >
                            {skill}
                          </span>
                        ))
                      ) : (
                        <span className="text-gray-500">No skills specified</span>
                      )}
                    </div>
                  </div>

                  {/* Recommendation */}
                  {match.recommendation && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-700 mb-2">Recommendation:</h4>
                      <p className="text-gray-600 bg-gray-50 p-3 rounded">
                        <ReactMarkdown>{match.recommendation}</ReactMarkdown> 
                      </p>
                    </div>
                  )}

                  {/* Skill Gap Analysis */}
                  {match.skill_gap_analysis && (
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Skill Gap Analysis:</h4>
                      <div className="text-gray-600 bg-gray-50 p-3 rounded">
                        <ReactMarkdown>{match.skill_gap_analysis}</ReactMarkdown>
                      </div>
                    </div>
                  )}

                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}