import React from 'react'
import './bannermessage.css'

export default function BannerMessage({ message, tabledata }) {
    return (
        <div className="alert alert-secondary alert-dismissible fade show" >
            <h4 className="alert-heading">Important Note</h4>
            <p>Per AWS : Dates with only a month and a year are approximate, and will be updated with the exact date when it is known. AWS updates the EOL dates time to time.</p>
            <hr />
            <p className="mb-0">
                {
                    message ? message : <>Review the Last Refresh Date, which is the time the last EOL data was fetched from AWS. The latest data can be fetched by clicking the refresh icon <i className="bi bi-arrow-clockwise"></i>.</>
                }
            </p>
                {
                    !tabledata || tabledata.length === 0 ? null : (
                        <>
                        <hr />
                            <table className="table-bordered table my-transparent-table">
                                <thead>
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">Engine</th>
                                        <th scope="col">Last Data Refresh Date from AWS</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {
                                        tabledata.map((row, index) => (
                                                <tr key={index}>
                                                    <td>{index}</td>
                                                    <td>{row.rds_engine_type}</td>
                                                    <td>{row.latest_refreshed_at}</td>
                                                </tr>
                                        ))
                                    }
                                </tbody>
                            </table>
                        </>
                    )
                }
        </div>
    )
}
