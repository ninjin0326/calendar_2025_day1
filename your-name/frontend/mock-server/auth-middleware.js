module.exports = (req, res, next) => {
  // Basic認証のシミュレーション
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Basic ')) {
    return res.status(401).json({
      message: 'Authorization header is required'
    });
  }

  try {
    const base64Credentials = authHeader.split(' ')[1];
    const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii');
    const [username, password] = credentials.split(':');
    
    // 簡易認証（実際のプロダクションでは使用しない）
    if (username && password) {
      // 認証成功として処理を続行
      req.user = { username };
      next();
    } else {
      return res.status(401).json({
        message: 'Invalid credentials'
      });
    }
  } catch (error) {
    return res.status(401).json({
      message: 'Invalid authorization header format'
    });
  }
}; 