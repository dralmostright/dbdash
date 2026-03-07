import { useEffect, useState } from "react";
import CountMetrics from "../../components/dashboard/CountMetrics"
import RdsApi from "../../api/RdsApi";

export default function RdsDownCount() {
    const [rdsdowntotalcount, setRdsDownTotalCount] = useState({
        title: "RDS Instances",
        subtitle: "Down",
        icon: "bi bi-database-fill-down",
        loading: true,
        loaderloc: "div",
        count: null,
        percentage: "4%",
        percentageColor: "text-success",
        iconcolor: "text-danger",
        linkpageurl: "/aws/rds/list-rds/down",
        errorMessage: null
    });

    useEffect(() => {
        const loadRdsDownTotalCount = async () => {
            try {
                /*
                function sleep(ms) {
                    return new Promise(resolve => setTimeout(resolve, ms));
                  }
                await sleep (100000)
                */
                setRdsDownTotalCount(prev => ({ ...prev, loading: true }));
                
                const res = await RdsApi.getRdsTotaldownCount();
                setRdsDownTotalCount(prev => ({
                    ...prev,
                    count: res.data.total_instances,
                }));
            } catch (error) {
                console.log(error)
                setRdsDownTotalCount(prev => ({
                    ...prev,
                    errorMessage: "Failed to load RDS Count",
                }));
            } finally {
                setRdsDownTotalCount(prev => ({
                    ...prev,
                    loading: false,
                }));
            }
        };
    
        loadRdsDownTotalCount();
    }, []);

    return (
        <div className="col-xxl-4 col-md-6">
            <CountMetrics metric={rdsdowntotalcount} />
        </div>
    )
}
