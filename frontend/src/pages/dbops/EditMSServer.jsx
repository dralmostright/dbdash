import { useState, useContext, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import FormInput from "../../components/forms/FormInput";
import { PageTitle } from "../../components/header/PageTitle";
import { MountList } from "./MountList";
import "./createmsserver.css"

export function EditMSServer() {
    const navigate = useNavigate();
    const { msdbs_id } = useParams(); 

    const [validated, setValidated] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const pagetitle = {
        title: "Server Details",
        parent: "Server Details",
        current: "Edit Server Details"
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

    useEffect(() => {
        const fetchServer = async () => {
        try {
            const res = await DbOpsApi.getserversamountll(msdbs_id);
            setServer(res.data.server);
            setMounts(res.data.mounts);
        } catch (err) {
            console.error(err);
            setError("Failed to load server data.");
        }
        };
        fetchServer();
    }, [msdbs_id]);    

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
        const newMounts = [...mounts];
        newMounts[index][e.target.name] = e.target.value;
        setMounts(newMounts);
    };

    const addMount = () => {
        setMounts([...mounts, { msdbsm_path: "", msdbsm_usage: "" }]);
    };
/*
    const removeMount = (index) => {
        const newMounts = mounts.filter((_, i) => i !== index);
        const delmount = mounts[index]
        if (delmount?.msdbsm_id) {
            console.log("Has valid id")
            deleteMount(delmount.msdbsm_id);
        }
        setMounts(newMounts);
    };

        async function deleteMount(msdbsm_id) {
            setError("");
            setSuccess("");
            setMLoading(true);
            try {
                await DbOpsApi.deleteserversmount(msdbs_id, payload);
                setSuccess("Mount point has been deleted successfully from repo");
                setTimeout(() => navigate("/jira/meta/list"), 1000);
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Deleting mount point from repo failed. Try again.");
            } finally {
                setMLoading(false);
            }
    }
*/

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
        const deleteMountFromRepo = async (msdbsm_id) => {
        try {
            await sleep(1000)
            await DbOpsApi.deleteserversmount(msdbsm_id);
            setSuccess("Mount point deleted successfully");
        } catch (err) {
            setError(
                err.response?.data?.message ||
                    "Deleting mount point failed. Try again."
            );
            throw err; // important for MountItem to handle failure
        }
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
        setValidated(true);
        if (form.checkValidity()) {
            setLoading(true);
            setError("");
            setSuccess("");
            try {
                await sleep(1000);
                await DbOpsApi.updateservermount(msdbs_id, payload);
                setSuccess("Server details has been updated successfully...");
                setTimeout(() => navigate("/msserver/meta/list"),10);
            } catch (err) {
                await sleep(1000);
                console.error(err);
                setError(err.response?.data?.message || "Updating Server details failed. Try again.");
            } finally {
                setLoading(false);
            }
        }
    };
    return (
        <>
            <title> DbDash - Update Server Details</title>
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
                                            <h5 className="card-title">Edit Server Metadata</h5>

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
                                                Mount Point Directory
                                                <button type="button" className="btn btn-sm btn-success" onClick={addMount}>
                                                    + Add Mount
                                                </button>
                                            </h5>
                                            <MountList
                                                mounts={mounts}
                                                setMounts={setMounts}
                                                mountInputs={mountInputs}
                                                handleMountChange={handleMountChange}
                                                deleteMountFromRepo={deleteMountFromRepo}
                                            />

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
                                                    "Update Server Metadata"
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