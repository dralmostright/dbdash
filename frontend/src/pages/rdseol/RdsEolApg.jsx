import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import EolTable from "../../components/rdsinst/EolTable";
import { Loading } from "../../components/utils/Loading";
import { PageTitle } from "../../components/header/PageTitle";
import { RdsEolList } from "./RdsEolList";

export function RdsEolApg() {
  const pagetitle = {
    title: "End of Life",
    parent: "EOL",
    current: "Rds Aurora Postgres",
  };

  const engine='aurora-postgresql'
  const macolumns = [
    { field: 'rds_ma_ver', header: 'PostgreSQL major version', sortable: 'sortable', visible: 'y'},
    { field: 'rds_ma_cm_release_date', header: 'Community release date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_ma_release_date', header: 'RDS release date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_ma_cm_eol', header: 'Community end of life date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_ma_rds_seol', header: 'RDS end of standard support date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_ma_1y_ex_eol', header: 'RDS start of Extended Support year 1 pricing', sortable: 'sortable', visible: 'n' },
    { field: 'rds_ma_3y_ex_eol', header: 'RDS start of Extended Support year 3 pricing', sortable: 'sortable', visible: 'n' },
    { field: 'rds_ma_ex_eol', header: 'RDS end of Extended Support date', sortable: 'sortable', visible: 'y' },
    { field: 'ma_row_created_at', header: 'Last Refresh Date', sortable: 'sortable', visible: 'y' },    
];  

const micolumns = [
    { field: 'rds_mi_ver', header: 'PostgreSQL minor version', sortable: 'sortable', visible: 'y'},
    { field: 'rds_mi_cr_date', header: 'Community release date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_mi_release_date', header: 'RDS release date', sortable: 'sortable', visible: 'y' },
    { field: 'rds_mi_seol', header: 'RDS end of standard support date', sortable: 'sortable', visible: 'y' },
    { field: 'mi_row_created_at', header: 'Last Refresh Date', sortable: 'sortable', visible: 'y' },
]; 
  return (
    <>
      <title> DbDash - EOL Aurora Postgresql</title>
      <Header />
      <Sidebar />
      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section">

            <div className="card">
                <RdsEolList engine={engine} version="major" columns={macolumns}/>
            </div>
            <div className="card">
                <RdsEolList engine={engine} version="minor" columns={micolumns}/>
            </div>       
        </section>
      </main>
      <Footer />
    </>
  );
}
