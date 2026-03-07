import { Link } from "react-router-dom";

const TableRow = ({ sn, columns = [], actions = [] , extras = [], status = []}) => {
    return (
        <tr>
            <td>{sn}</td>

            {columns.map((col, i) => (
                <td key={i}>{col}</td>
            ))}
            {extras.length > 0 && (
                <>
                    <td>
                    {extras.map((item, idx) => (
                        <button key={idx} type="button" style={{ marginRight: "1px" }} className="btn btn-outline-secondary btn-sm rounded-pill">{item}</button>
                    ))}
                    </td>
                </>
            )}

            {status.length > 0 && (
                            <>
                                <td>
                                {status.map((item, idx) => (
                                    <div className="text-center" key={idx}>
                                    <i
                                    className={`bi bi-arrow-${item ? "up" : "down"}-circle-fill ${item ? "text-success" : "text-danger"}`}
                                  ></i>
                                  </div>
                                ))}
                                </td>
                            </>
                        )}

            <td>
                <div
                    style={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: "4px",
                        justifyContent: "flex-start",
                        alignItems: "center",
                    }}
                >
                    {actions.map((action, idx) => {
                        const icon = (
                            <div className="icon">
                                <i className={action.iconname}></i>
                            </div>
                        );

                        if (action.path) {
                            return (
                                <Link
                                    key={idx}
                                    to={action.path}
                                    onClick={action.onClick}
                                    style={{ color: action.color }}
                                >
                                    {icon}
                                </Link>
                            );
                        }

                        return (
                            <button
                                key={idx}
                                onClick={action.onClick}
                                style={{
                                    color: action.color,
                                    background: "none",
                                    border: "none",
                                    cursor: "pointer",
                                    padding: 0,
                                }}
                            >
                                {icon}
                            </button>
                        );
                    })}
                </div>
            </td>
        </tr>
    );
};

export default TableRow;
