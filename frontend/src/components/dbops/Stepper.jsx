import './stepper.css'
export default function Stepper({ steps, currentStep }) {
  return (
    <div className="stepper-wrapper mb-4">
      {steps.map((step, index) => (
        <div key={index} className="stepper-item">
          
          {index !== 0 && (
            <div
              className={`stepper-line progress ${
                index <= currentStep ? "active" : ""
              }`}
            />
          )}

          <div
            className={`stepper-circle ${
              index <= currentStep ? "active" : ""
            }`}
          >
            {index + 1}
          </div>

          <small className="mt-1">{step}</small>
        </div>
      ))}
    </div>
  );
}
