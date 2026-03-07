import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { PageTitle } from "../../components/header/PageTitle";
import { Footer } from "../../components/footer/Footer";
import RdsInstanceTable from "../../components/rdsinst/RdsInstanceTable";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function ListRdsDown() {
    const [rdsData, setRdsData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const pagetitle = {
        title: "RDS Instances",
        parent: "RDS Intances",
        current: "Up Instances"
    }

    const columns = [
        { field: 'account_alias', header: 'Account Alias', sortable: 'sortable', visible: 'y'},
        { field: 'rds_identifier', header: 'RDS Identifier', sortable: 'sortable', visible: 'y' },
        { field: 'rds_engine', header: 'Engine', sortable: 'sortable', visible: 'y' },
        { field: 'rds_instcreatetime', header: 'Created At', sortable: 'sortable', visible: 'n' },
        { field: 'rds_enginever', header: 'Engine Version', sortable: 'sortable', visible: 'n' }
    ];   


    useEffect(() => {
        async function fetchData() {
            try {
                setLoading(true);
                const response = await RdsApi.getRdsList('down');
                setRdsData(response.data);
                setError(null);
            } catch (err) {
                console.error(err);
                setError("Failed to load up rds instances.");
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, []);

    return (
        <>
            <title> DbDash - Up Instances</title>
            <Header />
            <Sidebar />
            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />

                <section className="section dashboard">
                    <div className="row">
                        <div className="card">
                            <div className="card-body" style={{ minHeight: "500px"}}>
                                {
                                    error ? <ErrorCard message={error} />
                                        : loading 
                                            ? <Loading />
                                            : <RdsInstanceTable data={rdsData} columns={columns}/>
                                }
 
                            </div>
                        </div>

                    </div>
                </section>
            </main>
            <Footer />
        </>
    );
}