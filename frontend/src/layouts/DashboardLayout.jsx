import Navbar from "../components/Navbar/Navbar";

function DashboardLayout({ children }){

    return(

        <>

            <Navbar/>

            {children}

        </>

    )

}

export default DashboardLayout;