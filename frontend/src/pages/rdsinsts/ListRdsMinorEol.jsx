import { useEffect, useState } from "react";
import RdsApi from "../../api/RdsApi";
import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { PageTitle } from "../../components/header/PageTitle";
import { Footer } from "../../components/footer/Footer";
import RdsInstanceTable from "../../components/rdsinst/RdsInstanceTable";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";
import BannerMessage from "../../components/rdsinst/BannerMessage";
import { formatDateTime } from "../../components/utils/dateTImeUtils";

export function ListRdsMinorEol() {
    const [rdsData, setRdsData] = useState(null);
    const [lastRData, setLastRData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const pagetitle = {
        title: "RDS Instances",
        parent: "RDS Intances",
        current: "Minor End of Life"
    }

    const columns = [
        { field: 'account_alias', header: 'Account Alias', sortable: 'sortable', visible: 'y'},
        { field: 'rds_identifier', header: 'RDS Identifier', sortable: 'sortable', visible: 'y' },
        { field: 'rds_engine', header: 'Engine', sortable: 'sortable', visible: 'y' },
        { field: 'days_until_eol', header: 'Days Until EOL', sortable: 'sortable', visible: 'y' },
        { field: 'rds_mi_seol', header: 'Standard EOL Date', sortable: 'sortable', visible: 'y' },
        { field: 'mi_row_created_at', header: 'Last AWS refresh', sortable: 'sortable', visible: 'n' },
        { field: 'rds_instcreatetime', header: 'Created At', sortable: 'sortable', visible: 'n' },
        { field: 'rds_enginever', header: 'Engine Version', sortable: 'sortable', visible: 'n' }    ,            
    ];       

    const DATE_COLUMNS = [
    "mi_row_created_at",
    "rds_instcreatetime"
    ];

    const REFRESH_COLUMNS = [
    "latest_refreshed_at",
    ];

    const transformRows = (rows, cols) => {
    return rows.map((row) => {
        const newRow = { ...row };

        cols.forEach((col) => {
        if (newRow[col]) {
            newRow[col] = formatDateTime(newRow[col]);
        }
        });

        return newRow;
    });
    };

    useEffect(() => {
        async function fetchData() {
            try {
                setLoading(true);
                const response = await RdsApi.getRdsEolMinorList();
                //console.log(response.data)
                const formattedData = transformRows(response.data.minor_eol_data, DATE_COLUMNS);
                setRdsData(formattedData);
                const refreshData = transformRows(response.data.minor_refresh_date, REFRESH_COLUMNS);
                setLastRData(refreshData)
                setError(null);
            } catch (err) {
                console.error(err);
                setError("Failed to load instances for Minor End of life.");
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    //console.log(rdsData)

    return (
        <>
            <title> DbDash - Major EOL</title>
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
                                            : <>
                                            <BannerMessage tabledata={lastRData} message={ "Refresh the data going | RDS EOL > RDS [Postgres | Aurora Postgres .. and so on ] to get latest accurate data from AWS. Column Last AWS Refresh, show the last date the data was pulled AWS." }/>
                                            <RdsInstanceTable data={rdsData} columns={columns}/>
                                            </>
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