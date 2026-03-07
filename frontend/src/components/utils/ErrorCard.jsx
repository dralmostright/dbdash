import './Loading.css'
export default function ErrorCard({message}) {
        const locat = 'page';
        return (
            <div className={`d-flex justify-content-center ${ locat==='div' ? 'center-relative' : 'center-absolute'}`}>
                    <h4 className='text-danger'><i className="bi bi-exclamation-circle"></i> { message}</h4>
            </div>
  );
}
