import { useEffect, useState } from "react";
import CountMetrics from "../../components/dashboard/CountMetrics"
import RdsApi from "../../api/RdsApi";

export default function RdsCreatedCount() {
    const [rdscreatedcount, setRdsCreatedCount] = useState({
        title: "RDS Created",
        subtitle: "<= 30days",
        icon: "bi bi-database-fill-add text-dark",
        loading: true,
        loaderloc: "div",
        count: null,
        percentage: "4%",
        percentageColor: "text-success",
        iconcolor: "text-success",
        linkpageurl: "/aws/rds/list-rds/recent",
        errorMessage: null
    });

    useEffect(() => {
        const loadRdsUpCount = async () => {
            try {
              setRdsCreatedCount(prev => ({ ...prev, loading: true }));
                
                const res = await RdsApi.getRdsCreatedCount();
                setRdsCreatedCount(prev => ({
                    ...prev,
                    count: res.data.total_instances,
                }));
            } catch (error) {
                console.log(error)
                setRdsCreatedCount(prev => ({
                    ...prev,
                    errorMessage: "Failed to load RDS up Count",
                }));
            } finally {
              setRdsCreatedCount(prev => ({
                    ...prev,
                    loading: false,
                }));
            }
        };
    
        loadRdsUpCount();
    }, []);

    return (
        <div className="col-xxl-4 col-md-6">
            <CountMetrics metric={rdscreatedcount} />
        </div>
    )
}
