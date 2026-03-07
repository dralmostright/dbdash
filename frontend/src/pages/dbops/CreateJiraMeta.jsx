import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import UsersApi from "../../api/UsersApi";
import DbOpsApi from "../../api/DbOpsApi";
import { AuthContext } from "../../context/AuthContext";
import FormInput from "../../components/forms/FormInput";
import { PageTitle } from "../../components/header/PageTitle";

export function CreateJiraMeta() {
    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const [values, setValues] = useState({
        jira_meta_name: "",
        jira_user: "",
        jira_token: "",
        jira_api_url: "",
    });

    const pagetitle = {
        title: "Jira Meta",
        parent: "Jira Meta",
        current: "Add New Jira Meta"
    }

    const addUserInputs = [
        {
            id: 0,
            name: "jira_meta_name",
            type: "text",
            errorMessage: "Please provide name for Jira meta data.",
            label: "Jira Meta Name",
            required: true,
            pattern: "^[A-Za-z0-9]{3,16}$",
        },
        {
            id: 1,
            name: "jira_user",
            type: "text",
            errorMessage: "Please provide username used to login in Jira.",
            label: "Jira Email",
            required: true,
            pattern: "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$",
        },
        {
            id: 2,
            name: "jira_api_url",
            type: "text",
            errorMessage: "Please provide a valid API URL for jira.",
            label: "Jira API URL",
            required: true,
            pattern: "https?://.+",
        },        
        {
            id: 3,
            name: "jira_token",
            type: "text",
            errorMessage: "Please provide a valid Jira token to access Jira.",
            label: "Jira API Token",
            required: true,
            //pattern: "^[^\s]+$",
        },
    ];

    const onChange = (e) => {
        setValues({ ...values, [e.target.name]: e.target.value })
    }

    const handleAddUser = async (e) => {
        e.preventDefault();
        const form = e.currentTarget;

        if (!form.checkValidity()) {
            e.stopPropagation();
        }
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        setValidated(true);

        if (form.checkValidity()) {
            setLoading(true);
            setError("");
            setSuccess("");

            try {
                await DbOpsApi.createmetadata({
                    jira_meta_name: values.jira_meta_name,
                    jira_user: values.jira_user,
                    jira_token: values.jira_token,
                    jira_dbdash_uid: user.uid,
                    jira_api_url: values.jira_api_url,
                });

                setSuccess("Jira Meta added successfully...");
                setTimeout(() => navigate("/jira/meta/list"), 1000);
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Adding Metadata failed. Try again.");
            } finally {
                setLoading(false);
            }
        }
    };
    return (
        <>
            <title> DbDash - Add Jira Meta</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />
                <section className="section">
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Add New Jira Metadata</h5>
                                    {success && (

                                        <div className="alert alert-success text-center py-2">
                                            {success}
                                        </div>
                                    )}
                                    {error && (

                                        <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                            <i className="bi bi-exclamation-octagon me-1"></i>
                                            {error}
                                            <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                        </div>

                                    )}
                                    <form className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                                        noValidate
                                        onSubmit={handleAddUser}>
                                        {
                                            addUserInputs.map(
                                                (input) =>
                                                (
                                                    <FormInput key={input.id}
                                                        {...input}
                                                        value={values[input.name]}
                                                        onChange={onChange}
                                                    />
                                                )
                                            )
                                        }
                                        <div className="text-center">




                                            <button
                                                className="btn btn-primary w-100"
                                                type="submit"
                                                disabled={loading}
                                            >
                                                {loading ? (
                                                    <>
                                                        <span
                                                            className="spinner-border spinner-border-sm me-2"
                                                            role="status"
                                                            aria-hidden="true"
                                                        ></span>
                                                        Saving...
                                                    </>
                                                ) : (
                                                    "Create Jira Metadata"
                                                )}
                                            </button>

                                        </div>
                                    </form>

                                </div>
                            </div>
                        </div>

                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">No Labels / Placeholders as labels Form</h5>

                                </div>
                            </div>
                        </div>
                    </div>
                </section>

            </main>
            <Footer />
        </>
    )
}