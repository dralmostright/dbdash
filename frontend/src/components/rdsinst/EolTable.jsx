import React, { useState, useRef } from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { MultiSelect } from 'primereact/multiselect';
import "./RdsInstanceTable.css";
import "primereact/resources/themes/lara-light-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";

export default function EolTable({ data , columns }) {
  const [globalFilter, setGlobalFilter] = useState("");
  const dt = useRef(null);

  const initialVisible = columns.filter(column => column.visible === 'y');

  const [visibleColumns, setVisibleColumns] = useState(initialVisible);

  const exportCSV = () => {
    dt.current.exportCSV();
  };

  const onColumnToggle = (event) => {
    let selectedColumns = event.value;
    let orderedSelectedColumns = columns.filter((col) => selectedColumns.some((sCol) => sCol.field === col.field));

    setVisibleColumns(orderedSelectedColumns);
};

const header = <MultiSelect value={visibleColumns} options={columns} optionLabel="header" onChange={onColumnToggle} placeholder="Select Columns" className="sm:w-20rem" display="chip" style={{ maxWidth: "600px" }}/>;

  return (
    <>
      <div >
        <div
          className=""
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "10px",
          }}
        >
          <span className="p-input-icon-right searchbar">
            <i className="pi pi-search" />
            <InputText
              type="search"
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              placeholder="Search..."
            />
          </span>


          <Button
            type="button"
            onClick={exportCSV}
            className="btn btn-dark"
            style={{ padding: "8px"}}
          >
            Export <i className="bi bi-filetype-csv"></i>
          </Button>
        </div>
      </div>

      <div>
        <div className="">
          <DataTable
            ref={dt}
            value={data}
            paginator
            stripedRows
            size="small"
            rows={25}
            rowsPerPageOptions={[10, 25, 50, 100]}
            globalFilter={globalFilter}
            showGridlines
            header={header}
          >
            <Column
              header="S.N."
              body={(_, options) => options.rowIndex + 1}  
              style={{ width: "70px" }}
            />
                {visibleColumns.map((col) => (
                    <Column key={col.field} field={col.field} header={col.header} sortable={col.sortable}/>
                ))}
          </DataTable>
        </div>
      </div>
    </>
  );
}
