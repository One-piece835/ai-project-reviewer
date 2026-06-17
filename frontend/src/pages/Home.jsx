// import React from 'react'
import { useState } from "react";
import Navbar from "../components/Navbar";
import RepositoryForm from "../components/RepositoryForm";
import { reviewProject } from "../services/api";
import ReviewResult from "../components/ReviewResult";

const Home = () => {

  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastRepoUrl, setLastRepoUrl] = useState("");

  const handleAnalyze = async (repoUrl) => {
    // console.log(repoUrl);
    setLoading(true);
    setError("");
    setReview(null);
    try {
      const data = await reviewProject(repoUrl);
      console.log(data);
      setReview(data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        "Something went wrong"
    );
    }
    finally {
    setLoading(false);
}
};

const handleRetry = () => {
  if (lastRepoUrl) {
    handleAnalyze(lastRepoUrl);
  }
};

  return (
    <div className="w-full min-h-screen flex flex-col bg-[#020817]">
      <Navbar />
      <RepositoryForm onAnalyze={handleAnalyze} loading={loading}  />
      {loading && (
  <div className="bg-white rounded-xl shadow-md p-6 text-center">
    <h3 className="text-xl font-semibold">
      Analyzing Repository...
    </h3>

    <p className="text-gray-500 mt-2">
      This may take up to 1 minute.
    </p>
  </div>
)}
      {error && ( 
    <div className="text-center space-y-4">
    <p className="text-red-500 font-medium">
      {error}
    </p>

    <button
      onClick={handleRetry}
      className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg"
    >
      Retry Analysis
    </button>
  </div>
)}
      {review && (
    <ReviewResult review={review} />
)}

    </div>
  )
}

export default Home
