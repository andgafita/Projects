import java.awt.List;
import java.sql.Driver;
import java.util.ArrayList;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class TestLinks 
{
	public static String[] vector= {"Biblioteci", "Burse" , "Cantinele" , "Cazare", "Contact", "verifica", "Documente", "Ghidul", "academice", "Orientare", "Regulamente", "Reprezentarea", "Servicii"};
	public static void main(String[] args) throws InterruptedException
	{
		System.setProperty("webdriver.chrome.driver", "C:\\Users\\Tudor\\Desktop\\selenium\\chromedriver.exe");
		WebDriver driver=new ChromeDriver();
		driver.get("http://fiistudent.ddns.us/users/login/");
		
		driver.findElement(By.name("username")).sendKeys("teodora.calarasu@students.info.uaic.ro");
		driver.findElement(By.name("password")).sendKeys("valoare1");
		driver.findElement(By.xpath("//input[@type='submit']")).click();
		
		driver.get("http://fiistudent.ddns.us");
		driver.findElement(By.xpath("//a[@href='/resources/']")).click();
		
		
		java.util.List<WebElement> list=new ArrayList<>();
		list=driver.findElements(By.xpath("//ul[@class='resources-list']/li/a"));
		for(WebElement obj:list)
			System.out.println(obj.getText());
		
		for(String elem:vector)
		{
			String xpath="//a[@href and contains(text(),\"" +elem+ "\")]";
			driver.findElement(By.xpath(xpath)).click();
			driver.navigate().back();
			Thread.sleep(1000);
		}									
		
		
		vector= new String[]{"Orar", "Boards", "Noutati", "Resurse"};
		
		for(String elem:vector)
		{
			String xpath="//a[@href and contains(text(),\"" +elem+ "\")]";
			driver.findElement(By.xpath(xpath)).click();
			driver.navigate().back();
			Thread.sleep(1000);
		}
		
		driver.close();
		driver.quit();
	}
}
