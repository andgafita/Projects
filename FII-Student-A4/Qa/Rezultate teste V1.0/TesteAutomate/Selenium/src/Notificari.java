import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;

public class Notificari 
{
	public static String[] options= {"IP","MATEMATICA","Burse","Cazare","Contracte",""};
	public static void main(String[] args) throws InterruptedException
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/personalise/notificari']")).click();
		
		for (String value : options) 
		{
			for (int i = 0; i <= 2; i++) 
			{
				Select category = new Select(driver.findElement(By.name("category")));
				category.selectByIndex(i);
				Thread.sleep(1000);

				driver.findElement(By.name("keyword")).sendKeys(value);
				driver.findElement(By.xpath("//button[@type='submit']")).click();
			}
		}
		
		driver.findElement(By.xpath("//a[@href='/personalise/boards/1']")).click();
		Thread.sleep(1000);
		driver.navigate().back();
		driver.findElement(By.xpath("//a[@href='/news/1']")).click();
		Thread.sleep(1000);
		driver.navigate().back();
		driver.findElement(By.xpath("//a[@href='/news/1']")).click();
		Thread.sleep(1000);
		driver.navigate().back();
		driver.findElement(By.xpath("//a[@href='/news/3']")).click();
		Thread.sleep(1000);
		driver.navigate().back();
		
		driver.close();
		driver.quit();
	}
}
