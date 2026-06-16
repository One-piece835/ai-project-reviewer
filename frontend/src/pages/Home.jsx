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

  return (
    <div className="w-full min-h-screen flex flex-col bg-[#020817]">
      <Navbar />
      <RepositoryForm onAnalyze={handleAnalyze} />
      {loading && <div className="text-center py-10">
  <div className="animate-spin ..."></div>
  <p className="text-white">⏳ Analyzing Repository...</p>
</div>}
      {error && <div className="bg-red-100 border border-red-400 text-red-700 p-4 rounded-lg">
  {error}
</div>}
      {review && (
    <ReviewResult review={review} />
)}

    </div>
  )
}

export default Home
