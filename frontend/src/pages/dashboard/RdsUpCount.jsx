import { useEffect, useState } from "react";
import CountMetrics from "../../components/dashboard/CountMetrics"
import RdsApi from "../../api/RdsApi";

export default function RdsUpCount() {
    const [rdsupcount, setRdsUpCount] = useState({
        title: "RDS Instances",
        subtitle: "Up",
        icon: "bi bi-database-fill-up",
        loading: true,
        loaderloc: "div",
        count: null,
        percentage: "4%",
        percentageColor: "text-success",
        iconcolor: "text-success",
        linkpageurl: "/aws/rds/list-rds/up",
        errorMessage: null
    });

    useEffect(() => {
        const loadRdsUpCount = async () => {
            try {
                setRdsUpCount(prev => ({ ...prev, loading: true }));
                
                const res = await RdsApi.getRdsTotalUpCount();
                setRdsUpCount(prev => ({
                    ...prev,
                    count: res.data.total_instances,
                }));
            } catch (error) {
                console.log(error)
                setRdsUpCount(prev => ({
                    ...prev,
                    errorMessage: "Failed to load RDS up Count",
                }));
            } finally {
                setRdsUpCount(prev => ({
                    ...prev,
                    loading: false,
                }));
            }
        };
    
        loadRdsUpCount();
    }, []);

    return (
        <div className="col-xxl-4 col-md-6">
            <CountMetrics metric={rdsupcount} />
        </div>
    )
}
