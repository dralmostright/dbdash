import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import { PageTitle } from "../../components/header/PageTitle";
import { RdsHwList } from "./RdsHwList";

export function RdsRdsInst() {
  const pagetitle = {
    title: "Amazon RDS instance types",
    parent: "Instance Types",
    current: "Amazon RDS instance types",
  };

  const viewMode='rds'
  const columns = [
    { field: 'rds_hw_model', header: 'Model', sortable: 'sortable', visible: 'y'},
    { field: 'rds_hw_type', header: 'Type', sortable: 'sortable', visible: 'y' },
    { field: 'rds_hw_vcpu', header: 'vCPU', sortable: 'sortable', visible: 'y' },
    { field: 'rds_hw_core', header: 'Core Count', sortable: 'sortable', visible: 'n' },
    { field: 'rds_hw_mem', header: 'Memory (GiB)', sortable: 'sortable', visible: 'y' },
    { field: 'rds_hw_storage', header: 'Storage', sortable: 'sortable', visible: 'n' },
    { field: 'rds_hw_ebs_gbps', header: 'Dedicated EBS Bandwidth (Gbps)', sortable: 'sortable', visible: 'y' },
    { field: 'rds_hw_net_gbps', header: 'Network Performance (Gbps)', sortable: 'sortable', visible: 'n' }
];  
  return (
    <>
      <title> DbDash - Amazon RDS instance types</title>
      <Header />
      <Sidebar />
      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section">
          <div className="row">
            <div className="card">
                <RdsHwList viewMode={viewMode} columns={columns}/>
            </div>
          </div>         
        </section>
      </main>
      <Footer />
    </>
  );
}
