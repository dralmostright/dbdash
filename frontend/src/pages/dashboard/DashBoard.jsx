import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import RdsApi from "../../api/RdsApi";
import RdsTotalCount from "./RdsTotalCount";
import RdsUpCount from "./RdsUpCount";
import RdsDownCount from "./RdsDownCount";
import RdsCountPerAccount from "./RdsCountPerAccount";
import RdsEngineCount from "./RdsEngineCount";
import RdsAzCountPerAccount from "./RdsAzCountPerAccount";
import RdsEngineAcountCount from "./RdsEngineAcountCount";
import { PageTitle } from "../../components/header/PageTitle";
import RdsCreatedCount from "./RdsCreatedCount";
import RdsEngineMajorEol from "./RdsEngineMajorEol";
import RdsEngineMinorEol from "./RdsEngineMinorEol";
import { RdsEngineTypePerAcount } from "./RdsEngineTypePerAcount";
import { RdsAcctEngineCount } from "./RdsAcctEngineCount";
import { RecentActivity } from "./RecentActivity";
export function DashBoard() {
    const pagetitle = {
        title: "Dashboard",
        current: "Dashboard"
    }
    return (
        <>
            <title> DbDash - Dashboard</title>
            <Header />
            <Sidebar />

            <main id="main" className="main">
            <PageTitle pageprops={pagetitle} />

                <section className="section dashboard">
                    <div className="row">
                        <div className="col-lg-8">
                            <div className="row">
                                <RdsTotalCount />
                                <RdsUpCount />
                                <RdsDownCount />
                                <RdsCreatedCount />
                                <RdsEngineMajorEol />
                                <RdsEngineMinorEol />
                                <RdsAcctEngineCount />
                                
                                <RdsCountPerAccount />
                                <RdsAzCountPerAccount />
                                                        <RdsEngineAcountCount />
                                
                                { /*<RdsEngineTypePerAcount /> */ }

                            </div>
                        </div>

                        <div className="col-lg-4">

                        <RdsEngineCount />
                        <RecentActivity />
                        { /* <RdsEngineAcountCount /> */ }
                        </div>
                    </div>
                </section>
            </main>

            <Footer />            
        </>
    );
}
