import './Loading.css'
export function Loading({ tags }) {
    const locat = 'page';
    return (
        <div className={`d-flex justify-content-center ${ tags==='div' ? 'center-relative' : 'center-absolute'}`}>
                <span className="loader"></span>
        </div>
    )
}

/*
import './Loading.css'
export function Loading({ tags }) {
    console.log(tags)
    return (
        <div className={`d-flex justify-content-center ${ tags==='div' ? 'center-relative' : 'center-absolute'}`}>
                <span className="loader"></span>
        </div>
    )
}


export function Loading({ loader }) {
    const locat = loader ? 'div' : 'page';
    return (
        <div className={`d-flex justify-content-center ${ locat==='div' ? 'center-relative' : 'center-absolute'}`}>
                <span className="loader"></span>
        </div>
    )
}


export function Loading() {
    const locat = 'page';
    return (
        <div className={`d-flex justify-content-center ${ locat==='div' ? 'center-relative' : 'center-absolute'}`}>
                <span className="loader"></span>
        </div>
    )
}
    */