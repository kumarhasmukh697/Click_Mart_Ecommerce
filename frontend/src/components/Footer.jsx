export default function Footer() {
  return (
    <footer className="w-full py-4 border-t flex flex-col items-center text-sm text-gray-600 text-center">
      <p className="flex flex-col items-center gap-1">
        Developed with <span className="text-red-500">❤️</span> by{" "}
        <a
          href="https://www.linkedin.com/in/hasmukh-kumar-a20a4a233/"
          target="_blank"
          className="text-blue-600 hover:underline"
        >
          Hasmukh Kumar
        </a>
      </p>

      <div className="flex flex-col items-center gap-1 mt-2">
        <a
          href="mailto:developer.rathan@gmail.com"
          className="text-blue-600 hover:underline"
        >
          kumarhasmukh697@gmail.com{" "}
        </a>

        <span className="flex items-center gap-1 text-gray-500 text-sm">
          <i className="bi bi-geo-alt-fill" style={{ fontSize: "20px" }}></i>
          Surat(Gujarat), India
        </span>
      </div>
    </footer>
  );
}

