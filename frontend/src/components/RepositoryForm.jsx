import { useState } from "react";

const RepositoryForm = ({ onAnalyze, loading }) => {

  const [repoUrl, setRepoUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze(repoUrl);
};

  return (
    <div className="p-4 flex flex-col gap-6 justify-center items-center">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 justify-center items-center">
        <label className="font-bold text-2xl text-white">Paste GitHub Repository URL</label>
        <input
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          className="border-2 border-slate-700 text-white rounded-2xl p-2 w-full max-w-md focus:outline-none focus:border-cyan-500"
        />
        <button  type="submit" className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-2xl font-medium font-mono text-lg" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Project"}
        </button>
      </form>
    </div>
  );
};

export default RepositoryForm;
