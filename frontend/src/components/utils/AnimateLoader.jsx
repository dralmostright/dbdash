import './AnimateLoader.css'
export default function AnimateLoader() {
  return (
    <div style={{ justifyContent: "center", display: "flex" }}>
      <div className="loader-container">
  <div className="item">
    <img src="/src/assets/img/postgresql.png" />
  </div>

  <div className="item">
    <img src="https://i.pravatar.cc/600?img=5" />
  </div>

  <div className="item">
    <img src="/src/assets/img/oracle-database.png" />
  </div>

  <div className="item">
    <img src="https://i.pravatar.cc/600?img=8" />
  </div>

  <div className="item">
    <img src="https://i.pravatar.cc/600?img=9" />
  </div>

  <div className="item">
    <img src="https://i.pravatar.cc/600?img=10" />
  </div>

  <div className="item">
    <img src="https://i.pravatar.cc/600?img=19" />
  </div>
</div>
    </div>
  )
}
