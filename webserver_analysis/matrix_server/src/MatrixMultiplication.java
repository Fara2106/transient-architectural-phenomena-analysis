import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Random;

@WebServlet("/compute")
public class MatrixMultiplication extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Parse the "dimension" parameter from the request
        String dimensionParam = request.getParameter("dimension");
        int dimension;
        try {
            dimension = Integer.parseInt(dimensionParam);
            if (dimension <= 0) {
                throw new IllegalArgumentException("Dimension must be a positive integer.");
            }
        } catch (Exception e) {
            response.setContentType("text/html");
            response.getWriter().write("<html><body><h3>Invalid dimension parameter. Please provide a positive integer.</h3></body></html>");
            return;
        }

        // Generate two random square matrices of the given dimension
        int[][] matrixA = generateRandomMatrix(dimension);
        int[][] matrixB = generateRandomMatrix(dimension);

        // Perform matrix multiplication
        int[][] resultMatrix = multiplyMatrices(matrixA, matrixB);

        // Respond with success message
        response.setContentType("text/html");
        response.getWriter().write("<html><body>");
        response.getWriter().write("<h3>Matrix multiplication completed successfully!</h3>");
        response.getWriter().write("<p>Input dimension: " + dimension + "</p>");
        response.getWriter().write("<p>First element of result matrix: " + resultMatrix[0][0] + "</p>");
        response.getWriter().write("<p>Last element of result matrix: " + resultMatrix[dimension-1][dimension-1] + "</p>");
        response.getWriter().write("</body></html>");
    }

    private int[][] generateRandomMatrix(int dimension) {
        Random random = new Random();
        int[][] matrix = new int[dimension][dimension];
        for (int i = 0; i < dimension; i++) {
            for (int j = 0; j < dimension; j++) {
                matrix[i][j] = random.nextInt(100); // Random values between 0 and 99
            }
        }
        return matrix;
    }

    private int[][] multiplyMatrices(int[][] matrixA, int[][] matrixB) {
        int dimension = matrixA.length;
        int[][] result = new int[dimension][dimension];
        for (int i = 0; i < dimension; i++) {
            for (int j = 0; j < dimension; j++) {
                result[i][j] = 0;
                for (int k = 0; k < dimension; k++) {
                    result[i][j] += matrixA[i][k] * matrixB[k][j];
                }
            }
        }
        return result;
    }
}
