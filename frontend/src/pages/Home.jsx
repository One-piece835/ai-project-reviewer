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
      <RepositoryForm onAnalyze={handleAnalyze} loading={loading}  />
      {loading && (
        <div className="bg-white mx-auto rounded-xl max-w-md shadow-md p-3 text-center">
          <p className="text-gray-800 font-semibold">
            This may take up to 1 minute.
          </p>
        </div>
      )}
      {error && ( 
    <div className="text-center space-y-4">
    <p className="text-red-500 font-medium">
      {error}
    </p>
  </div>
)}
    {review && (
    <ReviewResult review={review} />
)}

    </div>
  )
}

export default Home
