import { useParams } from 'react-router';
import { Header } from "../../components/header/Header";
import { Sidebar } from '../../components/sidebar/Sidebar';
import { PageTitle } from "../../components/header/PageTitle";
import { Footer } from "../../components/footer/Footer";
import { JobStatus } from '../../components/dbops/JobStatus';
import { JobDetailLog } from '../../components/dbops/JobDetailLog';

export function ViewJobProgress() {
const {job_id} = useParams();
  const pagetitle = {
    title: "Provision Database Logs",
    parent: "Provision Database Logs",
    current: "View Job Detail",
  };
  return (
    <>
      <title> DbDash - Job Detail</title>
      <Header />
      <Sidebar />

      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section dashboard">
          <JobStatus job_id={job_id} />
          <JobDetailLog job_id={job_id} />
        </section>
      </main>

      <Footer />
    </>
  );
}
