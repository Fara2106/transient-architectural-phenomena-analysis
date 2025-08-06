import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

@WebServlet("/generate")
public class TableGenerator extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Get the number of rows (N) from the query parameter
        String rowsParam = request.getParameter("rows");
        int rows = (rowsParam != null) ? Integer.parseInt(rowsParam) : 5; // Default to 5 rows if not specified

        // Set the content type to HTML
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        // Generate the HTML table with random values
        Random random = new Random();
        out.println("<html>");
        out.println("<head><title>Random Table</title></head>");
        out.println("<body>");
        out.println("<h1>Generated Table with Random Values</h1>");
        out.println("<table border='1'>");

        // Table headers
        out.println("<tr><th>#</th><th>Random Value</th></tr>");

        // Table rows with random values
        for (int i = 1; i <= rows; i++) {
            int randomValue = random.nextInt(100); // Generate random values between 0-99
            out.println("<tr><td>" + i + "</td><td>" + randomValue + "</td></tr>");
        }

        out.println("</table>");
        out.println("</body>");
        out.println("</html>");
    }
}
