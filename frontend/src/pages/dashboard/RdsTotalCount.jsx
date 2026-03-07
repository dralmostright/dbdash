import { useEffect, useState } from "react";
import CountMetrics from "../../components/dashboard/CountMetrics"
import RdsApi from "../../api/RdsApi";

export default function RdsTotalCount() {
    const [rdstotalcount, setRdsTotalCount] = useState({
        title: "RDS Instances",
        subtitle: "Total",
        icon: "bi bi-database-fill",
        loading: true,
        loaderloc: "div",
        count: null,
        percentage: "4%",
        percentageColor: "text-success",
        description: "increase",
        linkpageurl: "/aws/rds/list-rds/all",
        errorMessage: null
    });

    useEffect(() => {
        const loadRdsTotalCount = async () => {
            try {
                
                setRdsTotalCount(prev => ({ ...prev, loading: true }));
                
                const res = await RdsApi.getRdsTotalCount();
                setRdsTotalCount(prev => ({
                    ...prev,
                    count: res.data.total_instances,
                }));
            } catch (error) {
                console.log(error)
                setRdsTotalCount(prev => ({
                    ...prev,
                    errorMessage: "Failed to load Total RDS Count",
                }));
            } finally {
                setRdsTotalCount(prev => ({
                    ...prev,
                    loading: false,
                }));
            }
        };
    
        loadRdsTotalCount();
    }, []);

    return (
        <div className="col-xxl-4 col-md-6">
            <CountMetrics metric={rdstotalcount} />
        </div>
    )
}
