import {
  useState,
  useEffect,
  forwardRef,
  useContext,
  useImperativeHandle,
} from "react";
import { AuthContext } from "../../context/AuthContext";
import DbOpsApi from "../../api/DbOpsApi";
import FormInput from "../forms/FormInput";

export const StepMetaJira = forwardRef(({ jiradata, setJiraData }, ref) => {
  const handleChange = (e) => {
    setJiraData({ ...jiradata, [e.target.name]: e.target.value });
  };

  const { user } = useContext(AuthContext);
  const [validated, setValidated] = useState(false);
  const [metaOptions, setMetaOptions] = useState([]);

  useEffect(() => {
    DbOpsApi.listmetadata(user.uid).then((res) => {
      setMetaOptions(res.data);
    });
  }, []);

  const jiraInputs = [
    {
      name: "jira_ticket",
      label: "Jira Ticket Number",
      type: "text",
      required: true,
      errorMessage: "Valid Jira ticket is required",
      pattern : "^[A-Z][A-Z0-9]{1,9}-[0-9]+$"
    },
    {
      name: "jira_id",
      label: "Select Jira Metadata",
      type: "select",
      required: true,
      errorMessage: "Metadata type is required",
      options: [
        { value: "", label: "Select type" },
        ...metaOptions.map((o) => ({
          value: o.jira_id,
          label: o.jira_meta_name,
        })),
      ],
    },
  ];

  useImperativeHandle(ref, () => ({
    validate() {
      setValidated(true);
      return document
        .getElementById("step-server-form")
        .checkValidity();
    },
  }));

  return (
    <div className="card col-lg-12" style={{ minHeight: "500px" }}>
      <div className="col-lg-6">
        <div className="row g-0" style={{ marginTop: "10px" }}>
          <h5>Jira Details</h5>
          <form id="step-server-form" className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`} noValidate>
            {jiraInputs.map((input) => (
              <FormInput
                key={input.name}
                {...input}
                value={jiradata[input.name] || ""}
                onChange={handleChange}
              />
            ))}
          </form>
        </div>
      </div>
      <div className="col-lg-6">
      </div>
    </div>
  );
});
