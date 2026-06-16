

const ProblemsCard = ({ review }) => {
  return (
    <div className="bg-slate-900 text-white rounded-xl shadow-md p-6">
  <h3 className="text-2xl font-bold mb-4">
    Problems Found
  </h3>

  <div className="space-y-4">
    {review.ai_review.problems_found?.map(
      (item, index) => (
        <div
          key={index}
          className="border border-slate-700 rounded-lg p-4"
        >
          <h4 className="font-bold text-red-400">
            {item.problem}
          </h4>

          <p className="mt-2">
            <strong>Why it matters:</strong>{" "}
            {item.why_it_matters}
          </p>

          <p className="mt-2">
            <strong>Suggestion:</strong>{" "}
            {item.suggestion}
          </p>

          <p className="mt-2">
            <strong>Example Fix:</strong>{" "}
            {item.example_fix}
          </p>
        </div>
      )
    )}
  </div>
</div>
  )
}

export default ProblemsCard
