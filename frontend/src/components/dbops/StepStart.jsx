export function StepStart() {
  return (
      <div className="card col-lg-12" style={{ minHeight: "500px" }}>
        <div className="row g-0">
          <div className="col-md-4" style={{marginTop: "10px"}}>
            <img src="/img/dbdash-3.png" className="img-fluid rounded-start"  />
          </div>
          <div className="col-md-8" style={{padding: "15px"}}>
              <h1>Welcome</h1>
              <p>This Wizard helps to provision database for MSSQL Server.</p>
          </div>
        </div>
      </div>
  );
}
