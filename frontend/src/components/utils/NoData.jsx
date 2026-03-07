import './Loading.css'
export function NoData() {
    const locat = 'page';
    return (
        <div className={`d-flex justify-content-center ${ locat==='div' ? 'center-relative' : 'center-absolute'}`}>
            <h4 className='text-warning'><i className="bi bi-graph-up-arrow"></i> {" "}No Data found</h4>
        </div>
    )
}