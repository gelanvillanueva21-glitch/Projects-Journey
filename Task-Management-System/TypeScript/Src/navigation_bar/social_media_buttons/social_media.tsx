
import { useState } from "react";
import { FacebookButton } from "./facebook_button";
import { InstagramButton } from "./instagram_button";
import { LinkedinButton } from "./linkedin_button";
import { GmailButton } from "./gmail_button";
import { TiktokButton } from "./tiktok_button";


export function SocialMediaButton() {
    const [socailMediaclick, setSocialMediaClick] = useState<"instagram" | "facebook" | "linkedin" | "gmail" | "tiktok" | null>(null);
    function redirectUrl() {
        if (socailMediaclick === "facebook")
            window.location.href = "https://facebook.com";
        if (socailMediaclick === "gmail")
            window.location.href = "https://mail.google.com";
        if (socailMediaclick === "instagram")
            window.location.href = "https://instagram.com";
        if (socailMediaclick === "linkedin")
            window.location.href = "https://linkedin.com";
        if (socailMediaclick === "tiktok")
            window.location.href = "https://tiktok.com";
    }

    return (
        <div className="button-container">
            <div className="button-header">
                <p className="header-context">
                    Social Media Contact
                </p>
            </div>
            <div className="button-box">
                <FacebookButton onClick={() => {
                    setSocialMediaClick("facebook");
                    redirectUrl();
                }}/>
                <InstagramButton onClick={() => {
                    setSocialMediaClick("instagram");
                    redirectUrl();
                }}/>
                <LinkedinButton onClick={() => {
                    setSocialMediaClick("linkedin");
                    redirectUrl();
                }}/>
                <GmailButton onClick={() => {
                    setSocialMediaClick("gmail");
                    redirectUrl();
                }}/>
                <TiktokButton onClick={() => {
                    setSocialMediaClick("tiktok");
                    redirectUrl();
                }}/>

            </div>
        </div>
    )

}







