import { Link } from "react-router";
import { Loading } from "../utils/Loading";
import { NoData } from "../utils/NoData";


export default function CountMetrics({ metric }) {
  if (metric.errorMessage)
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "158px" }}>
          <div className="card-body">
            <h5 className="card-title">
              {" "}
              {metric.title} <span>| {metric.subtitle} </span>{" "}
            </h5>
            <span className="text-danger d-flex justify-content-center align-items-center">
              <i className="bi bi-exclamation-circle me-2"></i>
              {metric.errorMessage}
            </span>
            {/* <ErrorCard message={metric.errorMessage} /> */}
          </div>
        </div>
      </div>
    );
{ /*
  if (metric.count === 0) {
    return (
      <div className="col-12">
        <div className="card" style={{ minHeight: "158px" }}>
          <div className="card-body">
            <h5 className="card-title">
              {" "}
              {metric.title} <span>| {metric.subtitle} </span>{" "}
            </h5>
            <span className='text-warning d-flex justify-content-center align-items-center'><i className="bi bi-graph-up-arrow me-2"></i> {" "}No Data found</span>
          </div>
        </div>
      </div>
    )
  }
*/ } 

  return metric.loading ? (
    <div className="card info-card sales-card" style={{ minHeight: "158px" }}>
      <div className="card-body">
        <Loading />
      </div>
    </div>
  ) : (
    <div className="card info-card sales-card">
      <div className="card-body">
        <h5 className="card-title">
          {metric.title} <span>| {metric.subtitle} </span>
        </h5>

        <div className="d-flex align-items-center">
          <div className="card-icon rounded-circle d-flex align-items-center justify-content-center">
            <i className={`${metric.icon} ${metric.iconcolor}`}></i>
          </div>
          <div className="ps-3">
            <h6>{metric.count}</h6>
            <span className="text-success small pt-1 fw-bold">
              <Link to={metric.linkpageurl}>
                {" "}
                <i className="bi bi-link-45deg"></i> View Detail
              </Link>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
