import { Navigate, useParams } from 'react-router';
import { Header } from "../../components/header/Header";
import { Sidebar } from '../../components/sidebar/Sidebar';
import { PageTitle } from "../../components/header/PageTitle";
import { Footer } from "../../components/footer/Footer";
import { ViewRdsAWSaccount } from './ViewRdsAWSaccount';
import { ViewRdsInstance } from './ViewRdsInstance';
import { ViewRdsHwConfig } from './ViewRdsHwConfig';
import { ViewSecRules } from './ViewSecRules';
import { ViewRdsParameters } from './ViewRdsParameters';

export function ViewRdsDetails() {
const {aid, riid } = useParams();
  const pagetitle = {
    title: "RDS Instances",
    parent: "RDS Intances",
    current: "View Rds Details",
  };
  return (
    <>
      <title> DbDash - Up Instances</title>
      <Header />
      <Sidebar />

      <main id="main" className="main">
        <PageTitle pageprops={pagetitle} />

        <section className="section dashboard">
          <ViewRdsAWSaccount aid={aid} />
          <ViewRdsInstance riid={riid} />
          <ViewRdsHwConfig riid={riid} />
          <ViewSecRules riid={riid} />
          <ViewRdsParameters riid={riid} />

        </section>
      </main>

      <Footer />
    </>
  );
}
