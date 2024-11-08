import "bootstrap/dist/css/bootstrap.min.css";
import HomeLayout from "./homelayout/HomeLayout";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Chatbot from "./chatbot/Chatbot";
import AddComponents from './addcomponents/AddComponents'

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <HomeLayout />,
      children: [
        {
          path: "/",
          element: <Chatbot />,
        },
        {
          path: "/addcomponents",
          element: <AddComponents />,
        },
      ],
    },
  ]);

  return (
    <div className="App ">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
