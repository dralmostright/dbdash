import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import { AuthContext } from "../../context/AuthContext";
import FormInput from "../../components/forms/FormInput";
import { PageTitle } from "../../components/header/PageTitle";
import "./createmsserver.css"

export function CreateMSServer() {
    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const pagetitle = {
        title: "Server Details",
        parent: "Server Details",
        current: "Add New Server Details"
    }

    const [server, setServer] = useState({
        msdbs_name: "",
        msdbs_host: "",
        msdbs_port: "",
        msdbs_database: "",
        msdbs_user: "",
        msdbs_password: "",
        msdbs_status: "",
    });

    const [mounts, setMounts] = useState([
        { msdbsm_path: "", msdbsm_usage: "" }
    ]);

    const serverInputs = [
        {
            name: "msdbs_name",
            label: "Server Name",
            type: "text",
            required: true,
            errorMessage: "Server name is required"
        },
        {
            name: "msdbs_host",
            label: "Server Host",
            type: "text",
            required: true,
            pattern: "^([0-9]{1,3}\\.){3}[0-9]{1,3}$",
            errorMessage: "Enter valid IP address"
        },
        {
            name: "msdbs_port",
            label: "Port",
            type: "text",
            required: true,
            pattern: "^[0-9]+$",
            errorMessage: "Enter valid Port numbe"
        },
        {
            name: "msdbs_database",
            label: "Default Database",
            type: "text",
            required: true,
            errorMessage: "Default database name is required"
        },
        {
            name: "msdbs_user",
            label: "Database User",
            type: "text",
            required: true,
            errorMessage: "Database Username is required"
        },
        {
            name: "msdbs_password",
            label: "Database Password",
            type: "password",
            required: true,
            errorMessage: "Database User password is required"
        },
        {
            name: "msdbs_status",
            label: "Server Status",
            type: "select",
            required: true,
            errorMessage: "Status is required",
            options: [
                { value: "", label: "Select Status" },
                { value: "true", label: "Active" },
                { value: "false", label: "Inactive" },
            ]

        }
    ];

    const mountInputs = [
        {
            name: "msdbsm_path",
            label: "Mount Path",
            type: "text",
            required: true,
            pattern: "^(?:[a-zA-Z]:\\\\|/).+",
            errorMessage: "Path must valid."
        },
        {
            name: "msdbsm_usage",
            label: "Usage (%)",
            type: "text",
            required: true,
            min: 0,
            max: 100,
            errorMessage: "Usage must be between 0 and 100"
        }
    ];

    const handleServerChange = (e) => {
        setServer({ ...server, [e.target.name]: e.target.value });
    };

    const handleMountChange = (index, e) => {
        const updated = [...mounts];
        updated[index][e.target.name] = e.target.value;
        setMounts(updated);
    };

    const addMount = () => {
        setMounts([...mounts, { path: "", usage: "" }]);
    };

    const removeMount = (index) => {
        setMounts(mounts.filter((_, i) => i !== index));
    };

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const form = e.currentTarget;

        if (!form.checkValidity()) {
            e.stopPropagation();
        }
        const payload = {
            server,
            mounts
        };
        //console.log(payload)
        //console.log(JSON.stringify(payload))
        //console.log("PAYLOAD:", JSON.stringify(payload, null, 2));
        setValidated(true);
        if (form.checkValidity()) {
            setLoading(true);
            setError("");
            setSuccess("");
            try {
                await DbOpsApi.createservermount(payload);
                setSuccess("Server details has been added successfully...");
                setTimeout(() => navigate("/msserver/meta/list"), 1000);
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Adding Server details failed. Try again.");
            } finally {
                setLoading(false);
            }
        }
    };
    return (
        <>
            <title> DbDash - Add Server</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />
                <section className="section">
                    <div className="row">
                        <div className="col-lg-12">
                            <div className="card">
                                <div className="card-body">
                                    {success && (

                                        <div className="alert alert-success alert-dismissible fade show" role="alert">
                                            <i className="bi bi bi-check-circle me-1"></i>
                                            {success}
                                        </div>
                                    )}
                                    {error && (

                                        <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                            <i className="bi bi-exclamation-octagon me-1"></i>
                                            {error}
                                        </div>

                                    )}
                                    <form className={`row g-3 needs-validation ${validated ? "was-validated" : ""}`}
                                        noValidate
                                        onSubmit={handleSubmit}>

                                        <div className="col-lg-6">
                                            <h5 className="card-title">Add New Server Metadata</h5>

                                            {serverInputs.map((input) => (
                                                <FormInput
                                                    key={input.name}
                                                    {...input}
                                                    value={server[input.name]}
                                                    onChange={handleServerChange}
                                                />
                                            ))}
                                        </div>
                                        <div className="col-lg-6">
                                            <h5 className="card-title d-flex justify-content-between align-items-center">
                                                Mount Points
                                                <button type="button" className="btn btn-sm btn-success" onClick={addMount}>
                                                    + Add Mount
                                                </button>
                                            </h5>

                                            {mounts.map((mount, index) => (
                                                <div key={index} className="border rounded p-3 mb-3">
                                                    <div className="d-flex justify-content-between">
                                                        <strong>Mount #{index + 1}</strong>
                                                        {mounts.length > 1 && (
                                                            <button
                                                                type="button"
                                                                className="btn btn-sm btn-danger"
                                                                onClick={() => removeMount(index)}
                                                            >
                                                                Remove
                                                            </button>
                                                        )}
                                                    </div>

                                                    {mountInputs.map((input) => (
                                                        <FormInput
                                                            key={input.name}
                                                            {...input}
                                                            value={mount[input.name]}
                                                            onChange={(e) => handleMountChange(index, e)}
                                                        />
                                                    ))}
                                                </div>
                                            ))}
                                        </div>

                                        <div className="text-center col-lg-6">

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
                                                    "Create Server Metadata"
                                                )}
                                            </button>

                                        </div>
                                    </form>

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