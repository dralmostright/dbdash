import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import { PageTitle } from "../../components/header/PageTitle";
import Stepper from "../../components/dbops/Stepper";
import { StepMounts } from "../../components/dbops/StepMounts";
import { StepStart } from "../../components/dbops/StepStart";
import { StepRetriveJira } from "../../components/dbops/StepRetriveJira";
import { StepMetaJira } from "../../components/dbops/StepMetaJira";
import { StepReview } from "../../components/dbops/StepReview";
import DbOpsApi from "../../api/DbOpsApi";
import LoaderSpin from "../../components/utils/LoaderSpin";
import './createmsserverwizard.css'

export default function CreateMSServerWizard() {
  const navigate = useNavigate();
  const steps = ["Start", "JiraMeta", "Jira", "Mounts", "Review"];
  const [currentStep, setCurrentStep] = useState(0);

  const [showModal, setShowModal] = useState(false);
  const [showSubmitJob, setShowSubmitJob] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [mounts, setMounts] = useState([]);
  const [serNmounts, setSerNMounts] = useState([]);  
  const [jiradata, setJiraData] = useState({
    jira_ticket: "",
    jira_id: "",
  });

  const [jiratdata, setJiraTData] = useState({
    jirat_ticket: "",
    jirat_summary: "",
    jirat_status: "",
    jirat_issue_type: "",
    jirat_assignee: "",
    jirat_num_sites: "",
    jirat_desktop_licenses: "",
    jirat_mobile_licenses: "",
    jirat_db_name: "",
    jirat_src_app_type: "",
    jirat_company_name: "",
    jirat_company_address: "",
    jirat_reporter: "",  
    jirat_created: ""           
  });  

  const pagetitle = {
        title: "Server Details",
        parent: "Server Details",
        current: "Add New Server Details"
    }

  const stepMetaJiraRef = useRef();
  const stepMountsRef = useRef();  

  const next = () => {
    if (currentStep === 1 && !stepMetaJiraRef.current.validate()) return;
    if (currentStep === 3 && !stepMountsRef.current.validate()) return;
    setCurrentStep((s) => s + 1);
  };

  const back = () => setCurrentStep((s) => s - 1);

  const confirmSubmit = async () => {
    setShowModal(true);
  };

  const submitJob = async (e) => {
    setShowModal(false);
    setShowSubmitJob(true);
    const payload = {
      jira_ticket_details: { 
        ...jiratdata,
        jirat_meta_id: jiradata.jira_id,
      },
      server_data: mounts,
    };
    try {
        //console.log(payload)
        const jobresponse = await DbOpsApi.provisiondb("exec", payload);
        setSuccess("Job has been submitted Successfully..");
        //console.log(jobresponse)
        setTimeout(() => navigate(`/provision/database/view-job/${jobresponse.data?.exec_job_id}`), 1000);
    } catch (err) {
        //await sleep(1000);
        console.error(err);
        setError(err.response?.data?.message || "Something went wrong submitting job. Try again/Check with team.");
    }
  };

  //console.log(success)
  console.log(error)

  return (
    <>
      <title> DbDash - Provision Database</title>
      <Header />
      <Sidebar />

      {showModal && (
        <div className="modal fade show" style={{ display: "block" }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content" style={{ zIndex: 5000 }}>
              <div className="modal-header">
                <h5 className="modal-title">Confirm Submission</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>

              <div className="modal-body">
                <p>Please confirm to Submit Provisioning Job?</p>
                <img src="/img/provision.png" className="img-fluid rounded-start"  />
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>

                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => {
                    setShowModal(false);
                    submitJob()
                  }}
                >
                  Confirm
                </button>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show"></div>
        </div>
      )}

      {showSubmitJob && (
        <div className="modal fade show" style={{ display: "block" }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content" style={{ zIndex: 5000 }}>
              <div className="modal-header">
                <h5 className="modal-title">Submitting Provisioning Job...</h5>
              </div>

              <div className="modal-body loader-center">
                {success ? (
                  <div className="d-flex flex-column align-items-center my-3">
                    <div
                      className={`status-icon-circle ${
                        success ? "status-success" : "status-failed"
                      } d-flex align-items-center justify-content-center`}
                    >
                      <i
                        className={`bi ${
                          success ? "bi-check-lg" : "bi-x-lg"
                        } status-icon-symbol`}
                      ></i>
                    </div>
                    <div
                      className={`mt-3 fw-semibold ${
                        success ? "text-success" : "text-danger"
                      }`}
                    >
                      {success}
                    </div>
                  </div>
                ) : error ? (
                  <div className="d-flex flex-column align-items-center my-3">
                    <div
                      className={`status-icon-circle ${
                        error ? "status-failed" : "status-failed"
                      } d-flex align-items-center justify-content-center`}
                    >
                      <i
                        className={`bi ${
                          error ? "bi-x-lg" : "bi-x-lg"
                        } status-icon-symbol`}
                      ></i>
                    </div>
                    <div
                      className={`mt-3 fw-semibold ${
                        error ? "text-danger" : "text-danger"
                      }`}
                    >
                      {error}
                    </div>
                  </div>
                ) : (
                  <LoaderSpin />
                )}
              </div>

              <div className="modal-footer">
                {(success || error) ? (
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setShowSubmitJob(false)}
                  >
                    Exit
                  </button>
                ) : (
                  <span className="text-muted">In progress...</span>
                )}
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show"></div>
        </div>
      )}

      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />
        <section className="section">
          <div className="row">
            <div className="col-lg-12">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Provision Database</h5>
                  <div className="row">
                    <Stepper steps={steps} currentStep={currentStep} />

                    {currentStep === 0 && <StepStart />}
                    {currentStep === 1 && <StepMetaJira ref={stepMetaJiraRef} jiradata={jiradata} setJiraData={setJiraData} />}
                    {currentStep === 2 && <StepRetriveJira jiratdata={jiratdata} setJiraTData={setJiraTData} jiramdata={jiradata}/>}
                    {currentStep === 3 && <StepMounts ref={stepMountsRef} mounts={mounts} setMounts={setMounts} serNmounts = {serNmounts} setSerNMounts={setSerNMounts}/>}
                    {currentStep === 4 && <StepReview jiratdata={jiratdata} serverdata={serNmounts} />}

                    <div className="text-center">
                      {currentStep > 0 && <button className="btn btn-secondary ms-4 aaa" onClick={back}>Back</button>}
                      {currentStep < steps.length - 1 && <button className="btn btn-primary ms-4" onClick={next}>Next</button>}
                      {currentStep === steps.length - 1 && <button className="btn btn-success ms-4" onClick={confirmSubmit}>Submit</button>}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
