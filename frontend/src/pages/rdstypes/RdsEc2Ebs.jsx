import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { Footer } from "../../components/footer/Footer";
import { PageTitle } from "../../components/header/PageTitle";
import { RdsHwList } from "./RdsHwList";

export function RdsEc2Ebs() {
  const pagetitle = {
    title: "Amazon RDS instance types",
    parent: "Instance Types",
    current: "Amazon RDS instance types (EBS volumes)",
  };

  const viewMode='ebs'
  const columns = [
    { field: 'ec2_hw_model', header: 'Instance size', sortable: 'sortable', visible: 'y'},
    { field: 'ec2_hw_type', header: 'Instance Type', sortable: 'sortable', visible: 'y' },
    { field: 'ec2_hw_basebandwm', header: 'Baseline bandwidth (Mbps)', sortable: 'sortable', visible: 'y' },
    { field: 'ec2_hw_maxbandwm', header: 'Maximum bandwidth (Mbps)', sortable: 'sortable', visible: 'n' },
    { field: 'ec2_hw_basethroputm', header: 'Baseline throughput (MB/s, 128 KiB I/O)', sortable: 'sortable', visible: 'y' },
    { field: 'ec2_hw_maxthroputm', header: 'Maximum throughput (MB/s, 128 KiB I/O)', sortable: 'sortable', visible: 'n' },
    { field: 'ec2_hw_baseiopsm', header: 'Baseline IOPS (16 KiB I/O)', sortable: 'sortable', visible: 'y' },
    { field: 'ec2_hw_maxiopswm', header: 'Maximum IOPS (16 KiB I/O)', sortable: 'sortable', visible: 'n' }
];  
  return (
    <>
      <title> DbDash - Amazon RDS instance types(EBS volumes)</title>
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
