import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import AwsAcctApi from "../../api/AwsAcctApi";
import FormInput from "../../components/forms/FormInput";
import { PageTitle } from "../../components/header/PageTitle";
import { Loading } from "../../components/utils/Loading";

export default function AddAwsAccount() {
    const navigate = useNavigate();

    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const [values, setValues] = useState({
        account_number: "",
        account_alias: "",
        account_org: "",
        account_status: "",
        account_az:""
    });

    const pagetitle = {
        title: "AWS Accounts",
        parent: "AWS Accounts",
        current: "Add New AWS Accounts"
    }

    const addAccountInputs = [
        {
            id: 0,
            name: "account_number",
            type: "text",
            errorMessage: "Please provide AWS account umber.",
            label: "Account Number",
            required: true,
            pattern: "^[A-Za-z0-9]{3,16}$",
        },
        {
            id: 1,
            name: "account_alias",
            type: "text",
            errorMessage: "Please provide Account Alias.",
            label: "Account Alias",
            required: true,
            pattern: "^[A-Za-z0-9 _-]{3,32}$",
        },
        {
            id: 2,
            name: "account_org",
            type: "text",
            errorMessage: "Please provide orginaztion name",
            label: "Account Org",
            required: true,
            pattern: "^[A-Za-z0-9 _-]{3,32}$",
        },
        {
            id: 3,
            name: "account_status",
            type: "select",
            label: "Account Status",
            required: true,
            errorMessage: "Please select status.",
            options: [
                { value: "", label: "Select a Status" },
                { value: "true", label: "Active" },
                { value: "false", label: "Inactive" },
            ]
        },
        {
            id: 4,
            name: "account_az",
            type: "text",
            errorMessage: "Please provide the az's.",
            label: "Account AZ ( e.g. us-west-1, us-east-1)",
            required: true,
            pattern: "^(?:[a-z]{2}-[a-z]+-\\d+)(?:,(?:[a-z]{2}-[a-z]+-\\d+))*$",
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
                await AwsAcctApi.createac({
                    account_number: values.account_number,
                    account_alias: values.account_alias,
                    account_org: values.account_org,
                    account_status: values.account_status,
                    account_az: values.account_az,
                });

                setSuccess("Aws Account added successfully...");
                setTimeout(() => navigate("/aws/accounts"), 500);
            } catch (err) {
                await sleep(500);
                console.error(err);
                setError(err.response?.data?.message || "Adding new Account failed. Try again.");
            } finally {
                setLoading(false);
            }
        }
    };
    return (
        <>
            <title> DbDash -AWS Accounts</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />
                <section className="section">
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Add New AWS Accounts</h5>
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
                                            addAccountInputs.map(
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
                                                    "Add Account"
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
