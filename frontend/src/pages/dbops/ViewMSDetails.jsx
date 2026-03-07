import { useState, useEffect } from "react";
import { useParams } from "react-router";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import DbOpsApi from "../../api/DbOpsApi";
import { PageTitle } from "../../components/header/PageTitle";
import { Loading } from "../../components/utils/Loading";
import TableRow from "../../components/table/TableRow";
import './viewmsdetails.css'

export function ViewMSDetails() {

    const { msdbs_id } = useParams();
    const [serverdata, SetServerData] = useState({ server: {}, mounts: [] });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const pagetitle = {
        title: "Server Details",
        parent: "Server Details",
        current: "View Server Details"
    }

    useEffect(() => {
        loadServerData();
    }, []);

    const loadServerData = () => {
        setLoading(true);

        DbOpsApi.getserversamountll(msdbs_id)
            .then(async (res) => {
                SetServerData(res.data);
            })
            .catch(() => {
                setMessage("Failed to load Servers info");
                setTimeout(() => setMessage(""), 1500);
                setLoading(false);
            })
            .finally(() => setLoading(false));
    };

    //console.log(serverdata)

    if (loading) return <Loading />;

    return (
        <>
            <title> DbDash - Server Details</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />
                <section className="section">
                    <div className="row">
                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Server Details</h5>
                                    {error && error !== "" && (
                                        <div className="alert alert-danger alert-dismissible fade show" role="alert">
                                            <i className="bi bi-exclamation-octagon me-1"></i>
                                            {error}
                                        </div>
                                    )}
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label ">Server Name</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_name}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label">Server IP/Host</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_host}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label ">Database Port</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_port}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label ">Default Database</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_database}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label ">Database User</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_user}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-3 col-md-4 label ">Status</div>
                                        <div class="col-lg-9 col-md-8">{serverdata.server.msdbs_status}</div>
                                    </div>

                                </div>
                            </div>
                        </div>

                        <div className="col-lg-6">
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Mount Points</h5>

                                    <table className="table table-hover table-sm table-bordered">
                                        <thead>
                                            <tr>
                                                <th scope="col">#</th>
                                                <th scope="col">Mount Point</th>
                                                <th scope="col">Usage</th>
                                            </tr>
                                        </thead>
                                        <tbody>

                                            {serverdata.mounts.map((server, index) => (
                                                <tr><td>{index + 1}</td><td>{server.msdbsm_path}</td><td>{server.msdbsm_usage}</td></tr>
                                            ))}
                                        </tbody>
                                    </table>
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