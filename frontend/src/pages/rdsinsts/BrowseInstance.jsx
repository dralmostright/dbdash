import { Header } from "../../components/header/Header";
import { Sidebar } from "../../components/sidebar/Sidebar";
import { PageTitle } from "../../components/header/PageTitle";
import { Footer } from "../../components/footer/Footer";

export function BrowseInstance() {
    const pagetitle = {
        title: "RDS Instances",
        parent: "RDS Intances",
        current: "Browse"
    }
    return (
        <>
            <title> DbDash - Up Instances</title>
            <Header />
            <Sidebar />

            <main id="main" className="main">
                <PageTitle pageprops={pagetitle} />

                <section className="section dashboard">
                    <div className="row">
                        <div className="card">
                            <div className="card-body">
                            <h5 class="card-title">Choose Filters</h5>
                                <form className="row g-3">
                                <div className="col-md-3">
                                        <label for="inputCity" className="form-label">Filter Name</label>
                                        <input type="text" className="form-control" id="inputCity" />
                                    </div>
                                    <div className="col-md-3">
                                        <label for="inputState" className="form-label">Filter Option</label>
                                        <select id="inputState" className="form-select">
                                            <option selected="">Choose...</option>
                                            <option>...</option>
                                        </select>
                                    </div>
                                    <div className="col-md-3">
                                        <label for="inputZip" className="form-label">Filter Name</label>
                                        <input type="text" className="form-control" id="inputZip" />
                                    </div>
                                    <div className="col-md-3">
                                        <label for="inputZip" className="form-label">Filter Option</label>
                                        <input type="text" className="form-control" id="inputZip" />
                                    </div>

                                    <div className="text-center">
                                        <button type="submit" style={{ marginRight: "5px"}} className="btn btn-primary">Submit</button>
                                        <button type="reset" className="btn btn-secondary">Reset</button>
                                    </div>
                                </form>
                            </div>
                        </div>

                    </div>
                </section>
            </main>

            <Footer />
        </>
    )
}
