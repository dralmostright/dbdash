import { useEffect, useState } from "react";
import CountMetrics from "../../components/dashboard/CountMetrics"
import RdsApi from "../../api/RdsApi";

export default function RdsEngineMajorEol() {
    const [rdsenginemajoreol, setRdsEngineMajorEol] = useState({
        title: "RDS End of Life",
        subtitle: "Major Ver",
        icon: "bi bi-database-fill-exclamation text-warning",
        loading: true,
        loaderloc: "div",
        count: null,
        percentage: "4%",
        percentageColor: "text-warning",
        description: "increase",
        linkpageurl: "/aws/rds/list-rds/eolmajor",
        errorMessage: null
    });

    useEffect(() => {
        const loadRdsMajorEol = async () => {
            try {
                
                setRdsEngineMajorEol(prev => ({ ...prev, loading: true }));
                
                const res = await RdsApi.getRdsEol('major');
                setRdsEngineMajorEol(prev => ({
                    ...prev,
                    count: res.data.eolcount,
                }));
            } catch (error) {
                console.log(error)
                setRdsEngineMajorEol(prev => ({
                    ...prev,
                    errorMessage: "Failed to load Major ver EOL",
                }));
            } finally {
                setRdsEngineMajorEol(prev => ({
                    ...prev,
                    loading: false,
                }));
            }
        };
    
        loadRdsMajorEol();
    }, []);

    return (
        <div className="col-xxl-4 col-md-6">
            <CountMetrics metric={rdsenginemajoreol} />
        </div>
    )
}
