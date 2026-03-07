import { NavLink } from "react-router";

export function PageTitle({ pageprops }) {
    return (
        <div className="pagetitle">
            <h1>{pageprops.title}</h1>
            <nav>
                <ol className="breadcrumb">
                    <li className="breadcrumb-item"><NavLink to="/">Home</NavLink></li>
                    { pageprops.parent && <li className="breadcrumb-item">{pageprops.parent}</li> }
                    <li className="breadcrumb-item active">{pageprops.current}</li>
                </ol>
            </nav>
        </div>
    )
}
