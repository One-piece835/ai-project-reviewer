// import React from 'react'

import ProblemsCard from "./ProblemsCard";

const ReviewResult = ({ review }) => {

  const score = review.ai_review.overall_score;

  const scoreColor =
    score >= 80
      ? "bg-green-600"
      : score >= 60
      ? "bg-yellow-500"
      : "bg-red-600";

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6 text-center">
        <h2 className="text-2xl font-bold">{review.metadata.name}</h2>

        <p className="text-gray-600 mt-2">{review.metadata.description}</p>
        <p className="text-md font-semibold">
          ⭐ {review.metadata.stars} stars
        </p>
        <p className="text-md font-semibold">🍴 {review.metadata.forks} Forks</p>
        <p className="text-md font-semibold">
         💻 {review.metadata.language}
        </p>
      </div>

      <div className={`bg-cyan-600 text-white rounded-xl shadow-md p-6 text-center ${scoreColor}`}>
        <h3 className="text-lg font-semibold">Overall Score</h3>

        <p className="text-5xl font-bold mt-2">
          {score}/100
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-2xl font-bold mb-4">
        Project Summary
      </h3>

  <p>
    {review.ai_review.project_summary}
  </p>
</div>

      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-2xl font-bold mb-4">Strengths</h3>

        <ul className="space-y-3">
          {review.ai_review.strengths?.map((strength, index) => (
            <li key={index} className="bg-green-100 p-3 rounded-lg">
              {strength}
            </li>
          ))}
        </ul>
      </div>

      <ProblemsCard review={review} />

      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-2xl font-bold mb-4">
          Resume Advice
        </h3>

        <ul className="space-y-3">
          {review.ai_review.resume_advice?.map(
            (advice, index) => (
              <li
                key={index}
                className="bg-blue-50 p-3 rounded-lg"
              >
                {advice}
              </li>
            )
          )}
        </ul>
</div>

<div className="bg-white rounded-xl shadow-md p-6">
  <h3 className="text-2xl font-bold mb-4">
    Improvements
  </h3>

  <ul className="space-y-3">
    {review.ai_review.improvements?.map(
      (improvement, index) => (
        <li
          key={index}
          className="bg-orange-50 p-3 rounded-lg"
        >
          {improvement}
        </li>
      )
    )}
  </ul>
</div>

    <div className="bg-white rounded-xl shadow-md p-6">
  <h3 className="text-2xl font-bold mb-4">
    Next Version Suggestions
  </h3>

  <ul className="space-y-3">
    {review.ai_review.next_version_suggestions?.map(
      (suggestion, index) => (
        <li
          key={index}
          className="bg-pink-100 p-3 rounded-lg"
        >
          {suggestion}
        </li>
      )
    )}
  </ul>
</div>

    </div>
  );
};

export default ReviewResult;
